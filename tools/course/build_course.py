# -*- coding: utf-8 -*-
"""
build_course.py - renders a free course from a JSON file in this folder (default course.json = "AI for Beginners").
    python tools/course/build_course.py ai-for-seniors      builds tools/course/ai-for-seniors.json into /ai-for-seniors/
Optional course keys: slug, short_name, signup_label, email_placeholder, large_text, hero_image (repo path of a photo),
and per lesson: image (repo path) + image_alt.

    python tools/course/build_course.py            validate + write pages
    python tools/course/build_course.py --check    validate only (links, tags, lengths)

Writes:
    ai-course/index.html            landing page with the email sign-up form   (indexed)
    ai-course/start/index.html      lesson hub shown after sign-up             (noindex)
    ai-course/lesson-N/index.html   the lessons                                (noindex)
    assets/img/ai-course.jpg        cover / social image
and adds /ai-course/ to sitemap.xml and the page generator's STATIC_URLS.

Header, nav and footer are lifted from tools/blog/post_template.html so the course always
matches the rest of the site. Sign-ups go through FormSubmit to novatoronto.ca@gmail.com
(subject "New AI course signup"), the visitor is redirected to the lesson hub and gets the
welcome email as FormSubmit's auto-response. The captcha is left ON for this form.
"""
import io, os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
BLOG_TOOLS = os.path.join(REPO, 'tools', 'blog')
sys.path.insert(0, BLOG_TOOLS)
DOMAIN = 'https://novatoronto.com'
FORM = 'https://formsubmit.co/novatoronto.ca@gmail.com'
ALLOWED_TAGS = {'p', 'a', 'strong', 'em', 'ul', 'ol', 'li', 'br'}
# Hosts that answer 400 to curl but are live. Each was opened in a browser and the cited claim read
# on the page before being listed here. help.instagram.com: checked 2026-10-02 (AI label rules).
VERIFIED_WALLS = {'help.instagram.com'}
e = html.escape


def fail(msg):
    print('COURSE CHECK FAILED: ' + msg)
    sys.exit(2)


def slug_of(course):
    return course.get('slug', 'ai-course')


def canon(course):
    return '%s/%s/' % (DOMAIN, slug_of(course))


def hero_rel(course):
    """Repo-relative path of the course cover: a supplied photo if it exists, else the drawn cover."""
    h = course.get('hero_image')
    if h and os.path.exists(os.path.join(REPO, h)):
        return h
    return 'assets/img/%s.jpg' % slug_of(course)


def hero_abs(course):
    return '%s/%s' % (DOMAIN, hero_rel(course))


def big_css(course):
    """Larger type for audiences that need it (course['large_text'] = true)."""
    if not course.get('large_text'):
        return ''
    return ('    <style>\n        .course p, .course li, .c-lesson span, .c-check label { font-size: 1.2rem; line-height: 1.85; }\n'
            '        .course h2 { font-size: 1.7rem; } .course h3, .c-lesson h3 { font-size: 1.25rem; }\n'
            '        .c-prompt { font-size: 1.05rem; } .c-note { font-size: 1rem; } .c-kicker { font-size: 1rem; }\n'
            '        .c-form input[type=text], .c-form input[type=email] { font-size: 1.15rem; min-height: 56px; }\n'
            '        .c-form button, .c-copy { font-size: 1.05rem; min-height: 52px; }\n    </style>\n')


def all_courses():
    """Every course JSON in this folder: [(slug, short_name, promise)]."""
    out = []
    for f in sorted(os.listdir(HERE)):
        if f.endswith('.json'):
            try:
                c = json.load(io.open(os.path.join(HERE, f), encoding='utf-8'))
            except Exception:
                continue
            if 'lessons' in c and 'landing' in c:
                out.append((slug_of(c), c.get('short_name') or c['course_title'].split(':')[0], c.get('promise', '')))
    return out


def read(p):
    return io.open(p, encoding='utf-8', newline='').read()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8', newline='').write(text.replace('\r\n', '\n'))


def words(s):
    return len(re.sub(r'<[^>]+>', ' ', s).split())


# ------------------------------------------------------------------ chrome ----
def chrome(prefix):
    """(header_html, footer_html) from the blog post template, re-based to `prefix`."""
    t = read(os.path.join(BLOG_TOOLS, 'post_template.html')).replace('\r\n', '\n')
    header = t[t.index('    <!--==================== HEADER'):t.index('    <!--==================== MAIN ====')]
    footer = t[t.index('    <!--==================== FOOTER'):t.index('    <!--==================== MAIN JS')]
    header = header.replace('<a href="../" class="nav__link active-link">', '<a href="@@BLOG@@" class="nav__link">')
    out = []
    for block in (header, footer):
        block = block.replace('../../', prefix).replace('@@BLOG@@', prefix + 'blog/')
        out.append(block)
    return out[0], out[1]


def head(prefix, title, desc, canonical, robots, image_abs, extra=''):
    return '''<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-17927080637"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());
        gtag('config', 'AW-17927080637');
        gtag('config', 'G-B064YQYKLC');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="%(desc)s">
    <meta name="author" content="Rujal Tuladhar">
    <meta name="robots" content="%(robots)s">
    <link rel="canonical" href="%(canonical)s">
    <meta property="og:type" content="website">
    <meta property="og:url" content="%(canonical)s">
    <meta property="og:title" content="%(title)s">
    <meta property="og:description" content="%(desc)s">
    <meta property="og:image" content="%(image)s">
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="%(title)s">
    <meta property="twitter:description" content="%(desc)s">
    <meta property="twitter:image" content="%(image)s">
    <link rel="stylesheet" href="https://unicons.iconscout.com/release/v4.0.0/css/line.css">
    <link rel="stylesheet" href="%(prefix)sassets/css/styles.css">
    <title>%(title)s</title>
    <link rel="icon" href="%(prefix)sassets/img/small_logo.png" type="image/png">
    <style>
        .course p { line-height: 1.8; margin-bottom: 1.15rem; color: var(--text-color); }
        .course p a, .course li a { color: var(--first-color-text); font-weight: 500; }
        .course ul, .course ol { margin: 0 0 1.25rem 1.35rem; color: var(--text-color); line-height: 1.7; }
        .course ul { list-style: disc; } .course ol { list-style: decimal; }
        .course li { margin-bottom: .45rem; }
        .course h2 { font-size: 1.45rem; color: var(--title-color); margin: 2.4rem 0 1rem; }
        .course h3 { font-size: 1.08rem; color: var(--title-color); margin: 1.4rem 0 .4rem; }
        .c-kicker { display: block; color: var(--first-color-text); font-weight: 700; text-transform: uppercase; letter-spacing: .04em; font-size: .85rem; margin-bottom: .5rem; }
        .c-box { background: hsl(199, 70%%, 97%%); border-left: 4px solid var(--first-color); border-radius: 0 .75rem .75rem 0; padding: 1rem 1.25rem; margin: 1.25rem 0 2rem; color: var(--title-color); line-height: 1.6; }
        .c-card { background: var(--container-color); border: 1px solid rgba(0, 150, 221, .18); border-radius: 1rem; padding: 1.25rem 1.4rem; margin-bottom: 1rem; }
        .c-exercise { background: var(--container-color); border: 2px solid var(--first-color); border-radius: 1.25rem; padding: 1.5rem 1.6rem; margin: 2rem 0; }
        .c-exercise h2 { margin-top: 0; }
        .c-prompt { position: relative; background: #0b1f3a; color: #e6f1fb; border-radius: .9rem; padding: 1.1rem 1.2rem 1.1rem; margin: .6rem 0 1.4rem; font-family: Consolas, 'Courier New', monospace; font-size: .9rem; line-height: 1.6; white-space: pre-wrap; }
        .c-copy { display: inline-flex; align-items: center; gap: .35rem; min-height: 44px; margin: 0 0 .2rem; padding: .4rem 1rem; border-radius: 2rem; border: 1px solid var(--first-color); background: #fff; color: var(--first-color-text); font-weight: 600; cursor: pointer; font-size: .85rem; }
        .c-check label { display: flex; gap: .7rem; align-items: flex-start; padding: .55rem 0; color: var(--text-color); line-height: 1.5; cursor: pointer; min-height: 44px; }
        .c-check input { width: 20px; height: 20px; margin-top: .15rem; flex: none; accent-color: hsl(199, 100%%, 33%%); }
        .c-nav { display: flex; flex-wrap: wrap; gap: .75rem; justify-content: space-between; margin: 2.5rem 0 1rem; }
        .c-lessons { display: grid; gap: .8rem; margin: 1.5rem 0 2rem; }
        .c-lesson { display: grid; grid-template-columns: 48px 1fr auto; gap: 1rem; align-items: center; text-decoration: none; background: var(--container-color); border: 1px solid rgba(0, 150, 221, .18); border-radius: 1rem; padding: 1rem 1.2rem; }
        .c-lesson b { display: flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: .9rem; background: rgba(0, 150, 221, .1); color: var(--first-color-text); font-size: 1.1rem; }
        .c-lesson h3 { margin: 0 0 .15rem; font-size: 1rem; color: var(--title-color); }
        .c-lesson span { color: var(--text-color-light); font-size: .85rem; }
        .c-lesson.done b { background: #16a34a; color: #fff; }
        .c-form { display: grid; gap: .7rem; max-width: 520px; }
        .c-form input[type=text], .c-form input[type=email] { padding: .9rem 1rem; border-radius: .9rem; border: 1px solid rgba(0, 150, 221, .35); background: #fff; color: #1b2532; font-size: 16px; min-height: 48px; width: 100%%; }
        .c-form button { border: none; cursor: pointer; min-height: 48px; justify-content: center; }
        .c-note { font-size: .82rem; color: var(--text-color-light); line-height: 1.5; margin: 0; }
        .c-hero { display: grid; gap: 2.5rem; align-items: center; }
        .c-panel { background: linear-gradient(160deg, hsl(199, 70%%, 97%%), #fff); border: 2px solid var(--first-color); border-radius: 1.5rem; padding: 1.75rem; }
        .c-ticks { list-style: none !important; margin-left: 0 !important; }
        .c-ticks li { position: relative; padding-left: 1.9rem; }
        .c-ticks li::before { content: '\\2713'; position: absolute; left: 0; top: 0; color: #16a34a; font-weight: 700; }
        @media (min-width: 900px) { .c-hero { grid-template-columns: 1.05fr .95fr; } }
    </style>
%(extra)s</head>

<body>
''' % {'prefix': prefix, 'title': e(title, quote=True), 'desc': e(desc, quote=True), 'canonical': canonical,
       'robots': robots, 'image': image_abs, 'extra': extra}


def tail(prefix, script=''):
    return '''
    <script src="%sassets/js/main.js"></script>
%s</body>

</html>
''' % (prefix, script)


def ld(data):
    return '    <script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False).replace('</', '<\\/') + '\n    </script>\n'


def form_html(course, cta, where):
    L = course['landing']
    start = canon(course) + 'start/'
    welcome = L['welcome_email'].replace('{START_URL}', start)
    return ('''<form class="c-form" action="%s" method="POST">
                        <input type="hidden" name="_subject" value="New AI course signup &mdash; novatoronto.com">
                        <input type="hidden" name="_template" value="table">
                        <input type="hidden" name="_next" value="%s?welcome=1">
                        <input type="hidden" name="_autoresponse" value="%s">
                        <input type="hidden" name="signup" value="Free AI course (%s)">
                        <input type="text" name="_honey" style="display: none" tabindex="-1" autocomplete="off">
                        <label class="sr-only" for="c-name-%s" style="position:absolute;left:-9999px">First name</label>
                        <input type="text" id="c-name-%s" name="name" placeholder="First name (optional)" autocomplete="given-name">
                        <label for="c-email-%s" style="position:absolute;left:-9999px">Email</label>
                        <input type="email" id="c-email-%s" name="email" required placeholder="you@business.com" autocomplete="email">
                        <button type="submit" class="button button--flex">%s <i class="uil uil-arrow-right button__icon"></i></button>
                        <p class="c-note">%s</p>
                    </form>''' % (FORM, start, e(welcome, quote=True), where, where, where, where, where, e(cta), e(L['form_note']))
            ).replace('Free AI course (', e(course.get('signup_label', 'Free AI course')) + ' (').replace(
              'you@business.com', e(course.get('email_placeholder', 'you@business.com'), quote=True))


# ------------------------------------------------------------------- pages ----
def landing(course):
    prefix = '../'
    L, lessons = course['landing'], course['lessons']
    header, footer = chrome(prefix)
    total_min = sum(int(l['minutes']) for l in lessons)
    schema = ld({'@context': 'https://schema.org', '@type': 'Course', 'name': course['course_title'],
                 'description': L['meta_description'], 'url': canon(course), 'inLanguage': 'en-CA',
                 'isAccessibleForFree': True,
                 'provider': {'@type': 'Organization', 'name': 'Nova Toronto', 'sameAs': DOMAIN + '/'},
                 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'CAD', 'category': 'Free'},
                 'hasCourseInstance': {'@type': 'CourseInstance', 'courseMode': 'Online',
                                       'courseWorkload': 'PT%dM' % total_min}})
    schema += ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in L['faq']]})
    rows = []
    for l in lessons:
        rows.append('''                    <div class="c-lesson"><b>%d</b><div><h3>%s</h3><span>%s</span></div><span>%d min</span></div>'''
                    % (l['number'], e(l['title']), e(l['objective']), int(l['minutes'])))
    body = '''    <main class="main">
        <section class="section" style="padding-top: 8rem;">
            <div class="container course c-hero">
                <div>
                    <span class="c-kicker">Free course &bull; %d lessons &bull; about %d minutes in total</span>
                    <h1 class="section__title" style="text-align: left; padding-top: 0; margin-bottom: 1rem;">%s</h1>
                    <p style="font-size: 1.1rem;">%s</p>
                    <ul class="c-ticks">
%s
                    </ul>
                </div>
                <div class="c-panel" id="signup">
                    <img src="../@@HERO@@" width="1200" height="630" alt="%s"
                        style="width: 100%%; height: auto; border-radius: 1rem; margin-bottom: 1.25rem;">
                    <h2 style="margin: 0 0 .4rem; font-size: 1.3rem;">Get the course free</h2>
                    <p style="margin-bottom: 1rem;">Enter your email and start lesson 1 right away.</p>
                    %s
                </div>
            </div>
        </section>

        <section class="section" style="padding-top: 0;">
            <div class="container course" style="max-width: 820px;">
                <h2>What is in the %d lessons</h2>
                <div class="c-lessons">
%s
                </div>

                <h2>Who this course is for</h2>
                <ul>
%s
                </ul>

                <h2>Common questions</h2>
%s

                <div class="c-panel" style="margin-top: 2.5rem;">
                    <h2 style="margin: 0 0 .4rem;">Start lesson 1 today</h2>
                    <p style="margin-bottom: 1rem;">%s</p>
                    %s
                </div>
                <p class="c-note" style="margin-top: 1.5rem;">Written by Rujal Tuladhar, Nova Toronto &bull; <a href="tel:+13653553133">365-355-3133</a> &bull; <a href="mailto:novatoronto.ca@gmail.com">novatoronto.ca@gmail.com</a></p>
            </div>
        </section>
    </main>

''' % (len(lessons), total_min, e(L['h1']), e(L['subhead']),
       '\n'.join('                        <li>%s</li>' % e(b) for b in L['learn_bullets']),
       e(course['course_title'], quote=True), form_html(course, 'Send me the free course', 'top'),
       len(lessons), '\n'.join(rows),
       '\n'.join('                    <li>%s</li>' % e(b) for b in L['who_for']),
       '\n'.join('                <h3>%s</h3>\n                <p>%s</p>' % (e(f['q']), e(f['a'])) for f in L['faq']),
       e(course['promise']), form_html(course, 'Send me the free course', 'bottom'))
    title = L['meta_title'] if 'Nova Toronto' in L['meta_title'] else L['meta_title'] + ' | Nova Toronto'
    body = body.replace('@@HERO@@', hero_rel(course))
    others = [c for c in all_courses() if c[0] != slug_of(course) and os.path.isdir(os.path.join(REPO, c[0]))]
    if others:
        more = '                <h2>More free courses</h2>\n                <div class="c-lessons">\n' + '\n'.join(
            '                    <a class="c-lesson" href="../%s/"><b><i class="uil uil-graduation-cap"></i></b><div><h3>%s</h3><span>%s</span></div><span>Free</span></a>'
            % (s, e(n), e(p)) for s, n, p in others) + '\n                </div>\n\n'
        mark = '                <p class="c-note" style="margin-top: 1.5rem;">Written by'
        body = body.replace(mark, more + mark, 1)
    return (head(prefix, title, L['meta_description'], canon(course),
                 'index, follow', hero_abs(course), schema + big_css(course)) + header + body + footer + tail(prefix))


def progress_js(course):
    return PROGRESS_JS.replace("'nova-ai-course'", "'nova-%s'" % slug_of(course))


PROGRESS_JS = '''    <script>
        (function () {
            var KEY = 'nova-ai-course';
            function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (err) { return {}; } }
            function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (err) { } }
            var state = load();
            document.querySelectorAll('[data-lesson-row]').forEach(function (row) {
                if (state['done' + row.getAttribute('data-lesson-row')]) { row.classList.add('done'); }
            });
            document.querySelectorAll('.c-check input').forEach(function (box) {
                var id = box.getAttribute('data-id');
                box.checked = !!state[id];
                box.addEventListener('change', function () { state[id] = box.checked; save(state); });
            });
            var done = document.getElementById('c-done');
            if (done) {
                var n = done.getAttribute('data-lesson');
                var paint = function () { done.textContent = state['done' + n] ? 'Lesson complete \\u2713' : 'Mark this lesson complete'; };
                paint();
                done.addEventListener('click', function () {
                    state['done' + n] = !state['done' + n]; save(state); paint();
                    if (state['done' + n] && typeof gtag === 'function') { gtag('event', 'course_lesson_complete', { lesson: n }); }
                });
            }
            document.querySelectorAll('.c-copy[data-copy]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var text = document.getElementById(btn.getAttribute('data-copy')).textContent;
                    var ok = function () { var old = btn.textContent; btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = old; }, 1600); };
                    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(ok, function () { }); }
                    else { var r = document.createRange(); r.selectNodeContents(document.getElementById(btn.getAttribute('data-copy'))); var s = getSelection(); s.removeAllRanges(); s.addRange(r); try { document.execCommand('copy'); ok(); } catch (err) { } }
                });
            });
            var w = document.getElementById('c-welcome');
            if (w && /[?&]welcome=1/.test(location.search)) { w.style.display = 'block'; }
        })();
    </script>
'''


def start_page(course):
    prefix = '../../'
    L, lessons = course['landing'], course['lessons']
    header, footer = chrome(prefix)
    rows = []
    for l in lessons:
        rows.append('''                    <a class="c-lesson" data-lesson-row="%d" href="../lesson-%d/"><b>%d</b><div><h3>%s</h3><span>%s</span></div><span>%d min</span></a>'''
                    % (l['number'], l['number'], l['number'], e(l['title']), e(l['objective']), int(l['minutes'])))
    body = '''    <main class="main">
        <section class="section" style="padding-top: 8rem;">
            <div class="container course" style="max-width: 820px;">
                <div class="c-box" id="c-welcome" style="display: none;"><strong>You are in.</strong> We have also emailed you this link so you can come back any time.</div>
                <span class="c-kicker">%s</span>
                <h1 class="section__title" style="text-align: left; padding-top: 0; margin-bottom: 1rem;">Your lessons</h1>
                <p>%s</p>
                <div class="c-lessons">
%s
                </div>
                <p class="c-note">Your progress is saved in this browser only. Questions? Email <a href="mailto:novatoronto.ca@gmail.com">novatoronto.ca@gmail.com</a> or call <a href="tel:+13653553133">365-355-3133</a>.</p>
            </div>
        </section>
    </main>

''' % (e(course['course_title']), e(L['start_page_intro']), '\n'.join(rows))
    return (head(prefix, 'Your lessons: ' + course['course_title'] + ' | Nova Toronto', L['meta_description'],
                 canon(course), 'noindex, follow', hero_abs(course), big_css(course))
            + header + body + footer + tail(prefix, progress_js(course)))


def lesson_page(course, l):
    prefix = '../../'
    lessons = course['lessons']
    n, total = l['number'], len(lessons)
    header, footer = chrome(prefix)
    sections = '\n'.join('                <h2>%s</h2>\n                %s' % (e(s['heading']), s['body_html'].strip()) for s in l['sections'])
    steps = '\n'.join('                        <li>%s</li>' % e(s) for s in l['exercise']['steps'])
    prompts = []
    for i, p in enumerate(l['prompts']):
        pid = 'p%d-%d' % (n, i)
        prompts.append('''                <h3>%s</h3>
                <button type="button" class="c-copy" data-copy="%s">Copy prompt</button>
                <div class="c-prompt" id="%s">%s</div>''' % (e(p['label']), pid, pid, e(p['text'])))
    checks = '\n'.join('                    <label><input type="checkbox" data-id="l%dc%d"><span>%s</span></label>' % (n, i, e(c))
                       for i, c in enumerate(l['checklist']))
    sources = ' &bull;\n'.join('                    <a href="%s" target="_blank" rel="noopener">%s</a>' % (e(s['url'], quote=True), e(s['label']))
                               for s in l['sources'])
    prev_ = ('<a href="../lesson-%d/" class="button button--small button--link"><i class="uil uil-arrow-left"></i> Lesson %d</a>' % (n - 1, n - 1)
             if n > 1 else '<a href="../start/" class="button button--small button--link"><i class="uil uil-arrow-left"></i> All lessons</a>')
    next_ = ('<a href="../lesson-%d/" class="button button--flex">Next: lesson %d <i class="uil uil-arrow-right button__icon"></i></a>' % (n + 1, n + 1)
             if n < total else '<a href="../../index.html#contact" class="button button--flex">Book a free 30-minute call <i class="uil uil-calendar-alt button__icon"></i></a>')
    finish = ''
    if n == total:
        finish = '''
                <div class="c-panel" style="margin-top: 2rem;">
                    <h2 style="margin-top: 0;">You finished the course</h2>
                    <p style="margin-bottom: 0;">%s</p>
                </div>''' % e(course['landing']['finish_note'])
    body = '''    <main class="main">
        <section class="section" style="padding-top: 8rem;">
            <div class="container course" style="max-width: 760px;">
                <a href="../start/" class="button button--small button--link" style="margin-bottom: 1rem;"><i class="uil uil-arrow-left"></i> All lessons</a>
                <span class="c-kicker">Lesson %d of %d &bull; about %d minutes</span>
                <h1 class="section__title" style="text-align: left; padding-top: 0; margin-bottom: 1rem;">%s</h1>
                <div class="c-box"><strong>By the end of this lesson:</strong> %s</div>

                %s

%s

                <div class="c-exercise">
                    <h2><i class="uil uil-pen"></i> Try it: %s</h2>
                    <ol>
%s
                    </ol>
                </div>

                <h2>Prompts you can copy</h2>
%s

                <h2>Before you move on</h2>
                <div class="c-check">
%s
                </div>

                <div class="c-box"><strong>Remember:</strong> %s</div>

                <p style="font-size: .9rem;">Sources checked for this lesson:
%s
                </p>
%s
                <div class="c-nav">
                    %s
                    <button type="button" class="c-copy" id="c-done" data-lesson="%d">Mark this lesson complete</button>
                    %s
                </div>
            </div>
        </section>
    </main>

''' % (n, total, int(l['minutes']), e(l['title']), e(l['objective']), l['intro_html'].strip(), sections,
       e(l['exercise']['title']), steps, '\n'.join(prompts), checks, e(l['takeaway']), sources, finish, prev_, n, next_)
    img = l.get('image')
    if img and os.path.exists(os.path.join(REPO, img)):
        pic = ('<img src="../../%s" width="1600" height="900" alt="%s" loading="lazy"\n'
               '                    style="width: 100%%; height: auto; border-radius: 1rem; margin-bottom: 1.5rem; box-shadow: 0 8px 30px rgba(0,70,120,0.12);">\n\n                '
               % (img, e(l.get('image_alt') or l['title'], quote=True)))
        mark = '<div class="c-box"><strong>By the end of this lesson:</strong>'
        body = body.replace(mark, pic + mark, 1)
    return (head(prefix, 'Lesson %d: %s | %s' % (n, l['title'], course.get('short_name') or course['course_title']), l['objective'][:150],
                 canon(course), 'noindex, follow', hero_abs(course), big_css(course))
            + header + body + footer + tail(prefix, progress_js(course)))


# ---------------------------------------------------------------- validate ----
def validate(course, check_links=True):
    L, lessons = course['landing'], course['lessons']
    if [l['number'] for l in lessons] != list(range(1, len(lessons) + 1)):
        fail('lessons must be numbered 1..N in order, got %s' % [l['number'] for l in lessons])
    if len(L['meta_title']) > 62 or len(L['meta_description']) > 160:
        fail('meta_title/meta_description too long (%d/%d)' % (len(L['meta_title']), len(L['meta_description'])))
    if '{START_URL}' not in L['welcome_email']:
        fail('welcome_email must contain {START_URL}')
    urls = set()
    for l in lessons:
        body = l['intro_html'] + ''.join(s['body_html'] for s in l['sections'])
        bad = set(t.lower() for t in re.findall(r'<\s*/?\s*([a-zA-Z0-9]+)', body)) - ALLOWED_TAGS
        if bad:
            fail('lesson %d: disallowed tags %s' % (l['number'], sorted(bad)))
        w = words(body)
        if not (450 <= w <= 1500):
            fail('lesson %d: %d words of teaching; expected 450-1500' % (l['number'], w))
        if not (3 <= len(l['exercise']['steps']) <= 8) or not l['prompts'] or not l['checklist']:
            fail('lesson %d: needs 3-8 exercise steps, at least one prompt and a checklist' % l['number'])
        for href in re.findall(r'href="([^"]+)"', body):
            if href.startswith('http'):
                urls.add(href)
            elif not href.startswith(('../', '/')):
                fail('lesson %d: internal link must start with ../ : %r' % (l['number'], href))
        for s in l['sources']:
            urls.add(s['url'])
        print('lesson %d: %4d words, %d steps, %d prompts, %d sources  %s' % (
            l['number'], w, len(l['exercise']['steps']), len(l['prompts']), len(l['sources']), l['title']))
    if check_links:
        import publish_post
        print('checking %d outbound links...' % len(urls))
        dead = []
        for u in sorted(urls):
            code, ok = publish_post.check_url(u)
            if not ok and publish_post.domain_of(u) in VERIFIED_WALLS:
                code, ok = code + ' wall', True      # live page that refuses non-browser clients
            if not ok:
                dead.append((u, code))
            print('  %s %s  %s' % ('ok  ' if ok else 'DEAD', code, u[:95]))
        if dead:
            fail('%d dead link(s): %s' % (len(dead), dead))
    print('course check passed: %d lessons' % len(lessons))


def main():
    """python build_course.py [course-file-or-slug] [--check] [--no-links]
    No name = course.json (the AI for Beginners course at /ai-course/)."""
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    name = names[0] if names else 'course'
    path = os.path.join(HERE, name if name.endswith('.json') else name + '.json')
    course = json.load(io.open(path, encoding='utf-8'))
    slug = slug_of(course)
    validate(course, check_links='--no-links' not in sys.argv)
    missing = [l['number'] for l in course['lessons'] if l.get('image') and not os.path.exists(os.path.join(REPO, l['image']))]
    if missing:
        print('note: lesson image file not found yet for lessons %s (pages build without them)' % missing)
    if '--check' in sys.argv:
        return
    if hero_rel(course) == 'assets/img/%s.jpg' % slug:          # no photo supplied: draw the cover
        import cover
        kb = cover.make_cover({'slug': 'free-ai-course-' + slug, 'category': 'Free course',
                               'cover_title': course.get('cover_title', course.get('short_name', 'Free AI Course'))},
                              course.get('date', '2026-10-02'), os.path.join(REPO, 'assets', 'img', slug + '.jpg'), motif='course') // 1024
        print('cover: assets/img/%s.jpg drawn (%d KB)' % (slug, kb))
    else:
        print('cover: using photo %s' % hero_rel(course))
    write(os.path.join(REPO, slug, 'index.html'), landing(course))
    write(os.path.join(REPO, slug, 'start', 'index.html'), start_page(course))
    for l in course['lessons']:
        write(os.path.join(REPO, slug, 'lesson-%d' % l['number'], 'index.html'), lesson_page(course, l))
    print('wrote %s/ (landing, start, %d lessons)' % (slug, len(course['lessons'])))

    sm = os.path.join(REPO, 'sitemap.xml')
    s = read(sm)
    loc = '<loc>%s</loc>' % canon(course)
    if loc not in s:
        nl = '\r\n' if s.count('\r\n') > s.count('\n') / 2 else '\n'
        i = s.find('\n', s.find('<urlset')) + 1
        entry = '  <url>%s    %s%s    <lastmod>%s</lastmod>%s    <priority>0.8</priority>%s  </url>%s' % (
            nl, loc, nl, course.get('date', '2026-10-02'), nl, nl, nl)
        io.open(sm, 'w', encoding='utf-8', newline='').write(s[:i] + entry + s[i:])
        print('sitemap: added /%s/' % slug)
    gen = os.path.join(REPO, 'tools', 'generate_local_pages.py')
    g = read(gen)
    anchor = '("blog/", 0.7),'
    if anchor in g and ('"%s/"' % slug) not in g:
        nl = '\r\n' if g.count('\r\n') > g.count('\n') / 2 else '\n'
        io.open(gen, 'w', encoding='utf-8', newline='').write(g.replace(anchor, anchor + nl + '    ("%s/", 0.8),' % slug, 1))
        print('generator: added %s/ to STATIC_URLS' % slug)


if __name__ == '__main__':
    main()
