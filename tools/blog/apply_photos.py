# -*- coding: utf-8 -*-
"""
apply_photos.py - give already-published posts their photo cover.

    python tools/blog/apply_photos.py            apply every photo found in tools/blog/_photos/
    python tools/blog/apply_photos.py --list     show which published posts have / lack a photo

For each published post with a master photo at tools/blog/_photos/<slug>.jpg ("/" in a slug becomes "--"):
  - writes the 1200x630 cover to assets/img/blog/<last-part-of-slug>.jpg
  - pipeline posts already point at that file, so nothing else changes
  - older hand-built posts get their first content image, og:image and twitter:image pointed at it
New posts need nothing: publish_post.py calls cover.make_cover, which uses the photo when one exists.
Nothing is committed here; the next publish (or a manual commit) carries the changes.
"""
import io, os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import cover


def main():
    log = json.load(io.open(os.path.join(HERE, 'published.json'), encoding='utf-8'))
    done = missing = 0
    for p in log:
        slug = p['slug']
        photo = cover.photo_for(slug)
        if '--list' in sys.argv:
            print('%-7s %s' % ('photo' if photo else 'MISSING', slug)); continue
        if not photo:
            missing += 1; continue
        name = slug.split('/')[-1]
        out_rel = 'assets/img/blog/%s.jpg' % name
        cover.make_photo_cover(photo, os.path.join(REPO, out_rel))
        page = os.path.join(REPO, 'blog', slug, 'index.html')
        if os.path.exists(page):
            raw = io.open(page, encoding='utf-8', newline='').read()
            depth = '../' * (slug.count('/') + 2)
            new_src, new_abs = depth + out_rel, 'https://novatoronto.com/' + out_rel
            if new_src not in raw:                       # older post: repoint hero + social images
                main_at = raw.find('<main')
                m = re.search(r'<img\b[^>]*\bsrc="([^"]+)"', raw[main_at:]) if main_at != -1 else None
                if m and 'NovaToronto' not in m.group(1):
                    s = main_at + m.start(1)
                    raw = raw[:s] + new_src + raw[s + len(m.group(1)):]
                raw = re.sub(r'(<meta property="(?:og|twitter):image" content=")[^"]*(")', r'\g<1>' + new_abs + r'\g<2>', raw)
                if 'property="og:image"' not in raw:     # text-only older post: no picture slot, so a share image only
                    t = re.search(r'([ \t]*)<meta property="og:title"[^>]*>(\r?\n)', raw)
                    if t:
                        raw = raw[:t.end()] + t.group(1) + '<meta property="og:image" content="%s">' % new_abs + t.group(2) + raw[t.end():]
                io.open(page, 'w', encoding='utf-8', newline='').write(raw)
        done += 1
        print('cover <- photo  %s' % slug)
    if '--list' not in sys.argv:
        print('%d post(s) updated, %d still without a photo' % (done, missing))


if __name__ == '__main__':
    main()
