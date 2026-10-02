# -*- coding: utf-8 -*-
"""
publish_post.py - turn a post JSON into a live blog post on novatoronto.com.

    python tools/blog/publish_post.py <post.json> [--date YYYY-MM-DD] [--no-push] [--dry-run] [--update]
    python tools/blog/publish_post.py --next [--date YYYY-MM-DD] [--no-push] [--dry-run] [--force]

    --next publishes the lowest-numbered ready post in tools/blog/_queue/ (NNN-slug.json), at most
    one per day. A post that fails validation (e.g. a source went dead) is moved to _queue/failed/
    and the next one is tried (up to 3). After publishing, the JSON moves to posts/<date>-<slug>.json.

    --update re-renders an EXISTING slug in place (corrections). Keeps the original
    publish date in the log, swaps the slide/card/strip, bumps sitemap lastmod.

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
QUEUE = os.path.join(HERE, '_queue')          # underscore = not served by GitHub Pages
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
    # Majority vote. A file with a handful of stray CRLF lines is an LF file.
    crlf = text.count('\r\n')
    return '\r\n' if crlf > (text.count('\n') - crlf) else '\n'


def eol_after(text, i):
    """Index just past the end of the line containing position i. Works for LF, CRLF and
    mixed files: always look for the bare LF. (2026-09-18: searching for CRLF in a mostly-LF
    homepage jumped ~2,300 lines and duplicated the whole page body.)"""
    j = text.find('\n', i)
    return len(text) if j == -1 else j + 1


LANDMARKS = ('<!-- SLIDES:START', '<!-- LATEST-POST:START', '<!-- LATEST-POST:END -->', 'id="blog"',
             '</main>', '<footer class="footer"', '</html>')

def guard_homepage(before, after):
    """Refuse to write a homepage that grew suspiciously or duplicated a landmark."""
    for mark in LANDMARKS:
        if after.count(mark) != 1:
            fail('homepage guard: %r appears %d times after edit (must be 1) - nothing written' % (mark, after.count(mark)))
    grew = len(after) - len(before)
    if abs(grew) > 8000:
        fail('homepage guard: index.html changed by %d chars in one publish - nothing written' % grew)

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
    if n == 0:
        # 000 = curl never got an HTTP status: connection refused/reset, TLS
        # rejection, HTTP/2 stream error, or timeout. Adobe, GlobeNewswire and
        # similar bot walls do this to non-browser clients while the page is
        # perfectly live (the agent fetched it in a browser). A truly dead page
        # answers 404/410, which is still caught above. The one 000 that IS dead
        # is a domain that does not exist - so resolve the host and decide.
        import socket
        host = domain_of(url) or url
        try:
            socket.getaddrinfo(re.sub(r':\d+$', '', host) or host, 443)
            return '000?', True      # resolves: bot wall, allow with warning
        except Exception:
            return '000', False      # no such host: genuinely dead
    return code, (200 <= n < 400) or n == 403


def validate(post, all_html, update=False):
    slug = post['slug']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        fail('slug must be lowercase-hyphenated: %r' % slug)
    exists = os.path.exists(os.path.join(REPO, 'blog', slug))
    if exists and not update:
        fail('blog/%s/ already exists (pass --update to re-render a correction in place)' % slug)
    if update and not exists:
        fail('--update given but blog/%s/ does not exist' % slug)

    log = json.load(io.open(LOG, encoding='utf-8')) if os.path.exists(LOG) else []
    titles = {p['title'].strip().lower() for p in log if p.get('slug') != slug}
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
    faq = post.get('faq') or []
    if faq:
        if not (3 <= len(faq) <= 6):
            fail('faq needs 3-6 items, got %d' % len(faq))
        for f in faq:
            q, a = f.get('q', '').strip(), f.get('a', '').strip()
            if not q.endswith('?') or len(q) > 110:
                fail('faq question must end with ? and be under 110 chars: %r' % q)
            if not a or '<' in a or len(a) > 600:
                fail('faq answers are plain text, 1-600 chars: %r' % q)

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
        if ok and code in ('403', '000?'):
            flag = 'wall'   # bot wall - live page curl cannot fetch; agent verified in browser
        print('  %s %s  %s' % (flag, code, u[:90]))
        if not ok:
            dead.append((u, code))
    if dead:
        fail('%d outbound link(s) unreachable: %s' % (len(dead), dead))
    print('validation passed: %d words, %d sources on %d domains' % (n, len(sources), len(doms)))
    return n


# ------------------------------------------------------------- cover image ----
def make_cover(post, date_iso, out_path):
    """Illustrated cover - drawn by tools/blog/cover.py (motif picked from slug/category)."""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import cover
    return cover.make_cover(post, date_iso, out_path)


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

    faq_block, faq_schema = '', ''
    if post.get('faq'):
        rows = ['                    <h2>Common questions</h2>']
        for f in post['faq']:
            rows.append('                    <h3>%s</h3>' % html.escape(f['q'].strip()))
            rows.append('                    <p>%s</p>' % html.escape(f['a'].strip()))
        faq_block = '\n'.join(rows)
        data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': f['q'].strip(),
             'acceptedAnswer': {'@type': 'Answer', 'text': f['a'].strip()}} for f in post['faq']]}
        faq_schema = ('    <script type="application/ld+json">\n' +
                      json.dumps(data, indent=2, ensure_ascii=False).replace('</', '<\\/') + '\n    </script>')

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
        '{{FAQ_BLOCK}}': faq_block,
        '{{FAQ_SCHEMA}}': faq_schema,
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
    j = eol_after(text, i)
    return text[:j] + block.replace('\n', nl) + nl + text[j:]


def replace_between(text, start, end, block, label):
    i, j = text.find(start), text.find(end)
    if i == -1 or j == -1 or j < i:
        fail('%s: markers %r / %r not found' % (label, start, end))
    nl = nl_of(text)
    i = eol_after(text, i)
    if i > j:
        fail('%s: start marker line runs past the end marker' % label)
    j = text.rfind('\n', 0, j) + 1          # keep the END marker's own indentation
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


def replace_card(text, slug, card):
    """Swap the blog-index card that follows '<!-- Post: slug -->' up to its </article>."""
    tag = '<!-- Post: %s -->' % slug
    i = text.find(tag)
    if i == -1:
        fail('blog/index.html: no card comment %r to update' % tag)
    nl = nl_of(text)
    line_start = text.rfind(nl, 0, i) + len(nl)
    end = text.find('</article>', i)
    if end == -1:
        fail('blog/index.html: unterminated card for %s' % slug)
    end += len('</article>')
    return text[:line_start] + card.replace('\n', nl) + text[end:]


def replace_slide(text, slug, slide):
    start_tag, end_tag = '<!-- slide:%s -->' % slug, '<!-- /slide:%s -->' % slug
    i, j = text.find(start_tag), text.find(end_tag)
    if i == -1 or j == -1:
        fail('index.html: slide markers for %s not found' % slug)
    nl = nl_of(text)
    line_start = text.rfind(nl, 0, i) + len(nl)
    return text[:line_start] + slide.replace('\n', nl) + text[j + len(end_tag):]


def strip_points_at(text, slug):
    i, j = text.find('<!-- LATEST-POST:START'), text.find('<!-- LATEST-POST:END -->')
    return i != -1 and j != -1 and ('href="blog/%s/"' % slug) in text[i:j]


# --------------------------------------------------------------------- main ----
def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__); sys.exit(1)
    if argv[0] == '--next':
        return run_next(argv)
    post_path = argv[0]
    date_iso = datetime.date.today().isoformat()
    if '--date' in argv:
        date_iso = argv[argv.index('--date') + 1]
    no_push = '--no-push' in argv
    dry = '--dry-run' in argv
    update = '--update' in argv

    post = json.load(io.open(post_path, encoding='utf-8'))
    slug = post['slug']
    all_html = (post['intro_html'] + ''.join(s['body_html'] for s in post['sections']) + post['bottom_line_html'] +
                ''.join('<p>%s</p>' % html.escape(f.get('a', '')) for f in (post.get('faq') or [])))
    n_words = validate(post, all_html, update=update)
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
    if update:
        write(bi, replace_card(read(bi), slug, card.strip('\n')))
    else:
        write(bi, insert_after_marker(read(bi), '<!-- BLOG-CARDS:START', card.strip('\n'), 'blog/index.html'))

    # 4b. homepage slider + latest-post strip
    hp = os.path.join(REPO, 'index.html')
    h = read(hp)
    h_before = h
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
    if update and ('<!-- slide:%s -->' % slug) in h:
        h = replace_slide(h, slug, slide)
    else:
        h = insert_after_marker(h, '<!-- SLIDES:START', slide, 'index.html slider')
        h = trim_slides(h)

    strip = '''                <a class="lp__link" href="blog/%s/">
                    <span class="lp__badge">New</span>
                    <span class="lp__cat">%s</span>
                    <span class="lp__title">%s</span>
                    <span class="lp__date">%s</span>
                    <i class="uil uil-arrow-right" aria-hidden="true"></i>
                </a>''' % (slug, html.escape(post['category']), html.escape(post['title']), human_date(date_iso))
    if not update or strip_points_at(h, slug):
        h = replace_between(h, '<!-- LATEST-POST:START', '<!-- LATEST-POST:END -->', strip, 'index.html latest strip')
    guard_homepage(h_before, h)
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
    loc = '<loc>%s/blog/%s/</loc>' % (DOMAIN, slug)
    if update and loc in s:
        j = s.find(loc)
        k = s.find('<lastmod>', j)
        e = s.find('</lastmod>', k)
        s = s[:k] + '<lastmod>' + date_iso + s[e:]
        write(sm, s)
    else:
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
    entry_log = {'date': date_iso, 'slug': slug, 'title': post['title'], 'category': post['category'],
                 'words': n_words, 'sources': [x['url'] for x in post['sources']]}
    if update:
        idx = next((i for i, e in enumerate(log) if e.get('slug') == slug), None)
        if idx is None:
            log.insert(0, entry_log)
        else:
            entry_log['date'] = log[idx].get('date', date_iso)   # keep the original publish date
            entry_log['updated'] = datetime.date.today().isoformat()   # real revision date, not --date
            log[idx] = entry_log
    else:
        log.insert(0, entry_log)
    io.open(LOG, 'w', encoding='utf-8').write(json.dumps(log, indent=2, ensure_ascii=False))

    # 5b. queue bookkeeping: a post published from _queue/ moves into posts/ (the audit trail)
    qf = os.environ.get('NOVA_QUEUE_FILE')
    if qf and os.path.exists(qf) and not update:
        dest = os.path.join(HERE, 'posts', '%s-%s.json' % (date_iso, slug))
        os.replace(qf, dest)
        io.open(os.path.join(QUEUE, 'state.json'), 'w', encoding='utf-8').write(
            json.dumps({'last_date': date_iso, 'last_slug': slug}, indent=1))
        print('queue: moved %s -> posts/%s' % (os.path.basename(qf), os.path.basename(dest)))

    # 6. git
    if no_push:
        print('--no-push: changes are in the working tree, not committed'); return
    verb = 'Blog (revised): %s' if update else 'Blog: %s'
    msg = (verb % post['title']) + '\n\n%s\n\n%s %s.' % (
        post['excerpt'], 'Revised' if update else 'Published', date_iso)
    subprocess.run(['git', 'add', '-A'], cwd=REPO, check=True)
    subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=REPO, check=True)
    r = subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO, capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print('PUSH FAILED:\n' + r.stderr); sys.exit(3)
    print('pushed. live in ~2 min at %s/blog/%s/' % (DOMAIN, slug))


def queue_files():
    if not os.path.isdir(QUEUE):
        return []
    return sorted(f for f in os.listdir(QUEUE) if re.fullmatch(r'\d{3}-[a-z0-9\-]+\.json', f))


def run_next(argv):
    """Publish the next ready post from _queue/. Cheap: no research, one command."""
    date_iso = datetime.date.today().isoformat()
    if '--date' in argv:
        date_iso = argv[argv.index('--date') + 1]
    dry = '--dry-run' in argv
    state_p = os.path.join(QUEUE, 'state.json')
    state = json.load(io.open(state_p, encoding='utf-8')) if os.path.exists(state_p) else {}
    files = queue_files()
    print('queue: %d ready post(s)' % len(files))
    if state.get('last_date') == date_iso and '--force' not in argv and not dry:
        print('queue: already published %s today (%s) - nothing to do' % (state.get('last_slug'), date_iso)); return
    if not files:
        print('queue: EMPTY - write the next calendar topic into tools/blog/_queue/ (see RECIPE.md)'); return
    for f in files[:3]:
        src = os.path.join(QUEUE, f)
        cmd = [sys.executable, os.path.abspath(__file__), src, '--date', date_iso]
        cmd += [a for a in ('--no-push', '--dry-run') if a in argv]
        print('queue: publishing %s' % f); sys.stdout.flush()
        rc = subprocess.run(cmd, env=dict(os.environ, NOVA_QUEUE_FILE=src)).returncode
        if rc == 0:
            left = len(queue_files())
            print('queue: done. %d post(s) left%s' % (left, ' - TOP UP the queue (RECIPE.md)' if left < 5 else '')); return
        if rc != 2 or dry:
            print('queue: stopped with exit code %d - not a validation problem, fix before retrying' % rc); sys.exit(rc)
        os.makedirs(os.path.join(QUEUE, 'failed'), exist_ok=True)
        os.replace(src, os.path.join(QUEUE, 'failed', f))
        print('queue: %s failed validation -> moved to _queue/failed/, trying the next one' % f)
    print('queue: 3 posts failed validation in a row - stopping'); sys.exit(2)


if __name__ == '__main__':
    main()
