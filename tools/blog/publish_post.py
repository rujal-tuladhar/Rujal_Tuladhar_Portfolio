# -*- coding: utf-8 -*-
"""
publish_post.py - turn a post JSON into a live blog post on novatoronto.com.

    python tools/blog/publish_post.py <post.json> [--date YYYY-MM-DD] [--no-push] [--dry-run]

What it does, in order:
  1. Validates the post: unique slug, length, >=4 external sources on >=3 domains,
     every outbound URL reachable, only allowed inline tags, allowed internal links.
     Any failure aborts BEFORE anything is written - an unattended run must never
     publish a half-broken post.
  2. Generates a branded 1200x630 cover image (assets/img/blog/<slug>.jpg).
  3. Renders blog/<slug>/index.html from tools/blog/post_template.html.
  4. Adds a card to blog/index.html, a slide to the homepage slider, updates the
     homepage "latest post" strip, sitemap.xml and the generator's STATIC_URLS.
  5. Appends to tools/blog/published.json (the dedupe log).
  6. git add / commit / push (skipped with --no-push; nothing is written with --dry-run).

Post JSON schema: see tools/blog/RECIPE.md.
"""
import io, os, re, sys, json, html, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
TEMPLATE = os.path.join(HERE, 'post_template.html')
LOG = os.path.join(HERE, 'published.json')
DOMAIN = 'https://novatoronto.com'

ALLOWED_CATEGORIES = {'AI Tools', 'AI News', 'AI Automation', 'Digital Marketing', 'Website Design'}
ALLOWED_TAGS = {'p', 'a', 'strong', 'em', 'ul', 'ol', 'li', 'br'}
ALLOWED_INTERNAL_PREFIXES = ('../../', '../', '/')
MIN_WORDS, MAX_WORDS = 800, 1800
MIN_SOURCES, MIN_DOMAINS = 4, 3
MAX_SLIDES = 8
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'


# ----------------------------------------------------------------- helpers ----
def read(path):
    return io.open(path, encoding='utf-8', newline='').read()

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='').write(text)

def nl_of(text):
    return '\r\n' if '\r\n' in text else '\n'

def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s)

def words(s):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", strip_tags(s)))

def attr(s):
    return html.escape(s, quote=True)

def domain_of(url):
    m = re.match(r'https?://([^/]+)', url)
    return (m.group(1).lower().replace('www.', '') if m else '')

def human_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime('%B ') + str(d.day) + d.strftime(', %Y')

def fail(msg):
    print('VALIDATION FAILED: ' + msg)
    sys.exit(2)


# -------------------------------------------------------------- validation ----
def check_url(url):
    """Return (http_code, ok). 403 counts as ok-with-warning: it is almost always a
    bot wall on a live page, and the researcher already fetched it in a browser."""
    try:
        code = subprocess.run(
            ['curl', '-s', '-L', '-o', os.devnull, '-A', UA, '--max-time', '25',
             '-w', '%{http_code}', url],
            capture_output=True, text=True, timeout=40).stdout.strip()
    except Exception:
        return '000', False
    try:
        n = int(code)
    except ValueError:
        return code, False
    return code, (200 <= n < 400) or n == 403


def validate(post, all_html):
    slug = post['slug']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        fail('slug must be lowercase-hyphenated: %r' % slug)
    if os.path.exists(os.path.join(REPO, 'blog', slug)):
        fail('blog/%s/ already exists' % slug)

    log = json.load(io.open(LOG, encoding='utf-8')) if os.path.exists(LOG) else []
    titles = {p['title'].strip().lower() for p in log}
    if post['title'].strip().lower() in titles:
        fail('a post with this exact title was already published')
    if len(post['title']) > 75:
        fail('title is %d chars; keep it under 75' % len(post['title']))
    if len(post['excerpt']) > 165:
        fail('excerpt is %d chars; keep it under 165' % len(post['excerpt']))
    if post['category'] not in ALLOWED_CATEGORIES:
        fail('category %r not in %s' % (post['category'], sorted(ALLOWED_CATEGORIES)))

    n = words(all_html)
    if n < MIN_WORDS:
        fail('body is %d words; minimum is %d' % (n, MIN_WORDS))
    if n > MAX_WORDS:
        fail('body is %d words; maximum is %d' % (n, MAX_WORDS))

    if not (3 <= len(post['glance']) <= 6):
        fail('glance needs 3-6 items, got %d' % len(post['glance']))
    if not (4 <= len(post['sections']) <= 7):
        fail('sections needs 4-7 items, got %d' % len(post['sections']))
    for g in post['glance']:
        if not re.fullmatch(r'uil-[a-z0-9\-]+', g['icon']):
            fail('glance icon %r is not a Unicons class' % g['icon'])

    tags = set(t.lower() for t in re.findall(r'<\s*/?\s*([a-zA-Z0-9]+)', all_html))
    bad = tags - ALLOWED_TAGS
    if bad:
        fail('disallowed HTML tags in body: %s' % sorted(bad))

    # every href, split into internal / external
    hrefs = re.findall(r'href="([^"]+)"', all_html)
    ext = [h for h in hrefs if h.startswith('http')]
    internal = [h for h in hrefs if not h.startswith('http')]
    for h in internal:
        if not h.startswith(ALLOWED_INTERNAL_PREFIXES):
            fail('internal link must be relative to the post folder (../../ or ../): %r' % h)
        target = h.split('#')[0]
        if target and not target.startswith('/'):
            p = os.path.normpath(os.path.join(REPO, 'blog', slug, target))
            if not (os.path.exists(p) or os.path.exists(os.path.join(p, 'index.html'))):
                fail('internal link target does not exist: %r' % h)

    sources = post['sources']
    if len(sources) < MIN_SOURCES:
        fail('need at least %d sources, got %d' % (MIN_SOURCES, len(sources)))
    doms = {domain_of(s['url']) for s in sources}
    if 'novatoronto.com' in doms:
        fail('sources must be external, not novatoronto.com')
    if len(doms) < MIN_DOMAINS:
        fail('sources must span at least %d distinct domains, got %s' % (MIN_DOMAINS, sorted(doms)))

    to_check = sorted(set(ext + [s['url'] for s in sources]))
    print('checking %d outbound links...' % len(to_check))
    dead = []
    for u in to_check:
        code, ok = check_url(u)
        flag = 'ok ' if ok else 'DEAD'
        if ok and code == '403':
            flag = '403?'
        print('  %s %s  %s' % (flag, code, u[:90]))
        if not ok:
            dead.append((u, code))
    if dead:
        fail('%d outbound link(s) unreachable: %s' % (len(dead), dead))
    print('validation passed: %d words, %d sources on %d domains' % (n, len(sources), len(doms)))
    return n


# ------------------------------------------------------------- cover image ----
def make_cover(post, date_iso, out_path):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    F_BOLD, F_REG = 'C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/segoeui.ttf'
    if not os.path.exists(F_BOLD):
        F_BOLD = F_REG = None
    def font(p, s):
        return ImageFont.truetype(p, s) if p else ImageFont.load_default()

    im = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for x in range(int(W * .58), W):
        t = (x - W * .58) / (W - W * .58)
        d.line([(x, 0), (x, H)], fill=(int(255 - 23 * t), int(255 - 10 * t), int(255 - 3 * t)))
    d.rectangle([0, H - 14, W, H], fill=(0, 150, 221))
    d.rectangle([0, 0, 10, H], fill=(0, 150, 221))

    logo_p = os.path.join(REPO, 'assets', 'img', 'NovaToronto.png')
    y = 58
    if os.path.exists(logo_p):
        logo = Image.open(logo_p).convert('RGBA')
        lw = 240
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        im.paste(logo, (72, y), logo)
        y += logo.height + 26

    f_eb = font(F_BOLD, 24)
    d.text((72, y), (post['category'] + '  ·  ' + human_date(date_iso)).upper(), font=f_eb, fill=(0, 115, 168))
    y += 46

    f_h = font(F_BOLD, 60)
    words_, lines, cur = post['cover_title'].split(), [], ''
    for w in words_:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f_h) <= 780:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    for line in lines[:3]:
        d.text((72, y), line, font=f_h, fill=(27, 37, 50))
        y += 70

    y += 10
    d.text((72, y), 'By Rujal Tuladhar  ·  novatoronto.com', font=font(F_REG, 26), fill=(83, 96, 110))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path, 'JPEG', quality=84, optimize=True, progressive=True)
    return os.path.getsize(out_path)


# ---------------------------------------------------------------- rendering ----
def render_post(post, date_iso, cover_rel, cover_abs):
    tpl = read(TEMPLATE)
    nl = nl_of(tpl)

    glance = []
    for g in post['glance']:
        glance.append('                        <div class="news-item"><i class="uil %s"></i>' % attr(g['icon']))
        glance.append('                            <div><h4>%s</h4><p>%s</p></div></div>' % (html.escape(g['heading']), html.escape(g['sub'])))

    sections = []
    for s in post['sections']:
        sections.append('                    <h2>%s</h2>' % html.escape(s['heading']))
        sections.append('                    ' + s['body_html'].strip())
        sections.append('                    <div class="takeaway"><strong>What it means for you:</strong> %s</div>' % html.escape(s['takeaway']))
        sections.append('')

    sources = []
    for i, s in enumerate(post['sources']):
        sep = ' &bull;' if i < len(post['sources']) - 1 else ''
        sources.append('                        <a href="%s" target="_blank" rel="noopener">%s</a>%s' % (attr(s['url']), html.escape(s['label']), sep))

    related = []
    for i, r in enumerate(post['related']):
        sep = ' &bull;' if i < len(post['related']) - 1 else ''
        related.append('                        <a href="%s">%s</a>%s' % (attr(r['href']), html.escape(r['label']), sep))

    glance_label = '%s at a glance' % post['title']
    subs = {
        '{{TITLE}}': html.escape(post['title']),
        '{{TITLE_ATTR}}': attr(post['title']),
        '{{TITLE_JSON}}': json.dumps(post['title']),
        '{{EXCERPT_ATTR}}': attr(post['excerpt']),
        '{{EXCERPT_JSON}}': json.dumps(post['excerpt']),
        '{{KEYWORDS_ATTR}}': attr(post['keywords']),
        '{{SLUG}}': post['slug'],
        '{{CATEGORY}}': html.escape(post['category']),
        '{{DATE_ISO}}': date_iso,
        '{{DATE_HUMAN}}': human_date(date_iso),
        '{{COVER_REL}}': cover_rel,
        '{{COVER_ABS}}': cover_abs,
        '{{INTRO}}': post['intro_html'].strip(),
        '{{GLANCE_LABEL_ATTR}}': attr(glance_label),
        '{{GLANCE_ITEMS}}': nl.join(glance),
        '{{GLANCE_CAPTION}}': html.escape(glance_label + ' &mdash; the short version.').replace('&amp;mdash;', '&mdash;'),
        '{{SECTIONS}}': nl.join(sections),
        '{{BOTTOM_LINE}}': post['bottom_line_html'].strip(),
        '{{SOURCES}}': nl.join(sources),
        '{{RELATED}}': nl.join(related),
    }
    out = tpl
    for k, v in subs.items():
        out = out.replace(k, v.replace('\n', nl) if '\n' in v else v)
    return out


def insert_after_marker(text, marker, block, label):
    i = text.find(marker)
    if i == -1:
        fail('%s: marker %r not found' % (label, marker))
    nl = nl_of(text)
    j = text.find(nl, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + nl + text[j:]


def replace_between(text, start, end, block, label):
    i, j = text.find(start), text.find(end)
    if i == -1 or j == -1 or j < i:
        fail('%s: markers %r / %r not found' % (label, start, end))
    nl = nl_of(text)
    i = text.find(nl, i) + len(nl)
    return text[:i] + block.replace('\n', nl) + nl + text[j:]


def trim_slides(text):
    """Keep the homepage slider to the newest MAX_SLIDES publisher-marked slides."""
    marks = [m.start() for m in re.finditer(r'<!-- slide:', text)]
    if len(marks) <= MAX_SLIDES:
        return text
    for start in reversed(marks[MAX_SLIDES:]):
        slug = re.match(r'<!-- slide:([^ ]+) -->', text[start:]).group(1)
        end_tag = '<!-- /slide:%s -->' % slug
        end = text.find(end_tag, start)
        if end == -1:
            continue
        end += len(end_tag)
        nl = nl_of(text)
        if text[end:end + len(nl)] == nl:
            end += len(nl)
        line_start = text.rfind(nl, 0, start) + len(nl)
        text = text[:line_start] + text[end:]
        print('  trimmed old slide: ' + slug)
    return text


# --------------------------------------------------------------------- main ----
def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__); sys.exit(1)
    post_path = argv[0]
    date_iso = datetime.date.today().isoformat()
    if '--date' in argv:
        date_iso = argv[argv.index('--date') + 1]
    no_push = '--no-push' in argv
    dry = '--dry-run' in argv

    post = json.load(io.open(post_path, encoding='utf-8'))
    slug = post['slug']
    all_html = post['intro_html'] + ''.join(s['body_html'] for s in post['sections']) + post['bottom_line_html']
    n_words = validate(post, all_html)
    if dry:
        print('dry run - nothing written'); return

    # 2. cover
    cover_rel = '../../assets/img/blog/%s.jpg' % slug
    cover_abs = '%s/assets/img/blog/%s.jpg' % (DOMAIN, slug)
    size = make_cover(post, date_iso, os.path.join(REPO, 'assets', 'img', 'blog', slug + '.jpg'))
    print('cover: %d KB' % (size // 1024))

    # 3. post page
    write(os.path.join(REPO, 'blog', slug, 'index.html'), render_post(post, date_iso, cover_rel, cover_abs))
    print('wrote blog/%s/index.html' % slug)

    # 4a. blog index card
    bi = os.path.join(REPO, 'blog', 'index.html')
    card = '''
                <!-- Post: %s -->
                <article
                    style="background: var(--container-color); padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <span style="font-size: 0.8rem; color: var(--first-color-text); font-weight: bold; text-transform: uppercase;">%s</span>
                    <h3 style="margin: 1rem 0;">%s</h3>
                    <p style="margin-bottom: 1.5rem; color: var(--text-color);">%s</p>
                    <a href="./%s/" class="button button--small button--link">Read More <i class="uil uil-arrow-right"></i></a>
                </article>
''' % (slug, html.escape(post['category']), html.escape(post['title']), html.escape(post['excerpt']), slug)
    write(bi, insert_after_marker(read(bi), '<!-- BLOG-CARDS:START -->', card.strip('\n'), 'blog/index.html'))

    # 4b. homepage slider + latest-post strip
    hp = os.path.join(REPO, 'index.html')
    h = read(hp)
    slide = '''                    <!-- slide:%s -->
                    <div class="swiper-slide">
                        <article class="blog__card">
                            <div class="blog__img-wrapper">
                                <span class="blog__category">%s</span>
                                <img src="assets/img/blog/%s.jpg" width="1200" height="630" loading="lazy" alt="%s" class="blog__img">
                            </div>
                            <div class="blog__content">
                                <h3 class="blog__title">%s</h3>
                                <p class="blog__desc">%s</p>
                                <div class="blog__footer">
                                    <a href="blog/%s/" class="blog__btn">Read Story <i class="uil uil-arrow-right"></i></a>
                                </div>
                            </div>
                        </article>
                    </div>
                    <!-- /slide:%s -->''' % (slug, html.escape(post['category']), slug, attr(post['title']),
                                            html.escape(post['title']), html.escape(post['excerpt']), slug, slug)
    h = insert_after_marker(h, '<!-- SLIDES:START -->', slide, 'index.html slider')
    h = trim_slides(h)

    strip = '''                <a class="lp__link" href="blog/%s/">
                    <span class="lp__badge">New</span>
                    <span class="lp__cat">%s</span>
                    <span class="lp__title">%s</span>
                    <span class="lp__date">%s</span>
                    <i class="uil uil-arrow-right" aria-hidden="true"></i>
                </a>''' % (slug, html.escape(post['category']), html.escape(post['title']), human_date(date_iso))
    h = replace_between(h, '<!-- LATEST-POST:START -->', '<!-- LATEST-POST:END -->', strip, 'index.html latest strip')
    write(hp, h)
    print('updated index.html slider + latest-post strip')

    # 4c. sitemap + generator
    sm = os.path.join(REPO, 'sitemap.xml')
    s = read(sm)
    entry = '''  <url>
    <loc>%s/blog/%s/</loc>
    <lastmod>%s</lastmod>
    <priority>0.6</priority>
  </url>''' % (DOMAIN, slug, date_iso)
    i = s.find('<urlset')
    i = s.find(nl_of(s), i) + len(nl_of(s))
    write(sm, s[:i] + entry.replace('\n', nl_of(s)) + nl_of(s) + s[i:])

    gen = os.path.join(REPO, 'tools', 'generate_local_pages.py')
    g = read(gen)
    anchor = '("blog/", 0.7),'
    if anchor in g and ('"blog/%s/"' % slug) not in g:
        g = g.replace(anchor, anchor + nl_of(g) + '    ("blog/%s/", 0.6),' % slug, 1)
        write(gen, g)
    print('updated sitemap.xml + STATIC_URLS')

    # 5. log
    log = json.load(io.open(LOG, encoding='utf-8')) if os.path.exists(LOG) else []
    log.insert(0, {'date': date_iso, 'slug': slug, 'title': post['title'], 'category': post['category'],
                   'words': n_words, 'sources': [x['url'] for x in post['sources']]})
    io.open(LOG, 'w', encoding='utf-8').write(json.dumps(log, indent=2, ensure_ascii=False))

    # 6. git
    if no_push:
        print('--no-push: changes are in the working tree, not committed'); return
    msg = 'Blog: %s\n\n%s\n\nPublished %s by the daily blog task.' % (post['title'], post['excerpt'], date_iso)
    subprocess.run(['git', 'add', '-A'], cwd=REPO, check=True)
    subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=REPO, check=True)
    r = subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO, capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print('PUSH FAILED:\n' + r.stderr); sys.exit(3)
    print('pushed. live in ~2 min at %s/blog/%s/' % (DOMAIN, slug))


if __name__ == '__main__':
    main()
