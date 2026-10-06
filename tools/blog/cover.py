# -*- coding: utf-8 -*-
"""
cover.py - illustrated 1200x630 blog covers for novatoronto.com.

Every cover is drawn from scratch with PIL (no stock photos, nothing to licence):
a deep-blue gradient, soft light blobs, the title on the left, and a glass-style
illustration on the right chosen from the post's slug/category:

    video      play-button film card          (video, reel, ad creative)
    phone      phone with voice waveform      (receptionist, call, voice, answering)
    shop       storefront with product tiles  (shopify, ecommerce, amazon, walmart, store)
    chart      rising bars + trend line       (ads, marketing, seo, budget, roi, leads)
    browser    website wireframe              (website, web design, landing, page)
    flow       connected automation nodes     (automation, workflow, ai, chat, agent)
    news       stacked headline cards         (news, week)
    shield     shield + checklist             (law, casl, privacy, pipeda, aoda, rules, tax)
    course     open lesson cards + cap        (course, lesson, beginner)

Variation (tilt, blob positions, accent) is seeded from the slug, so a post always
gets the same cover and two posts in the same family still look different.

    python tools/blog/cover.py            renders one sample of every motif to _cover_samples/
"""
import os, sys, math, hashlib, random

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
S = 2                       # supersample factor
W, H = 1200 * S, 630 * S
NAVY, DEEP, BLUE, SKY, MINT, AMBER, PINK = (9, 26, 51), (6, 52, 98), (0, 150, 221), (120, 205, 255), (94, 234, 212), (255, 196, 87), (255, 122, 162)
F_BOLD, F_SEMI, F_REG = 'C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/seguisb.ttf', 'C:/Windows/Fonts/segoeui.ttf'

MOTIFS = [
    ('course', ('course', 'lesson', 'beginner', 'learn-ai')),
    ('news', ('ai-news', 'news-for', 'this-week', 'week-of')),
    ('shield', ('casl', 'pipeda', 'privacy', 'aoda', 'accessib', 'law', 'legal', 'rules', 'compliance', 'hst', 'tax', 'bill-', 'disclosure')),
    ('video', ('video', 'reel', 'tiktok', 'creative')),
    ('phone', ('receptionist', 'answering', 'phone', 'call', 'voice', 'voicemail')),
    ('shop', ('shopify', 'woocommerce', 'ecommerce', 'e-commerce', 'online-store', 'amazon', 'walmart', 'seller', 'product', 'shipping', 'checkout', 'store')),
    ('chart', ('google-ads', 'meta-ads', 'facebook-ads', 'ads', 'marketing', 'seo', 'budget', 'roi', 'roas', 'leads', 'reviews', 'google-business', 'ppc', 'campaign')),
    ('browser', ('website', 'web-design', 'landing', 'wordpress', 'wix', 'squarespace', 'homepage', 'site', 'domain', 'hosting')),
    ('flow', ('automation', 'automate', 'workflow', 'chat', 'agent', 'ai-', 'crm', 'zapier', 'n8n')),
]
CATEGORY_DEFAULT = {'Website Design': 'browser', 'Digital Marketing': 'chart', 'AI Automation': 'flow',
                    'AI News': 'news', 'AI Tools': 'flow'}


def pick_motif(slug, category):
    s = slug.lower()
    for name, keys in MOTIFS:
        if any(k in s for k in keys):
            return name
    return CATEGORY_DEFAULT.get(category, 'flow')


def _font(path, size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _rr(draw, box, r, **kw):
    draw.rounded_rectangle([int(v) for v in box], radius=int(r), **kw)


def _layer():
    from PIL import Image
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def _glass(base, box, r, fill=(255, 255, 255, 34), outline=(255, 255, 255, 90), shadow=True):
    """Frosted card: soft drop shadow + translucent fill + hairline border."""
    from PIL import ImageDraw, ImageFilter, Image
    if shadow:
        sh = _layer()
        _rr(ImageDraw.Draw(sh), (box[0] + 10 * S, box[1] + 18 * S, box[2] + 10 * S, box[3] + 18 * S), r, fill=(2, 12, 30, 120))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18 * S)))
    lay = _layer()
    _rr(ImageDraw.Draw(lay), box, r, fill=fill, outline=outline, width=2 * S)
    base.alpha_composite(lay)


def _background(rng):
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.new('RGB', (W, H), NAVY)
    px = im.load()
    for y in range(0, H, 2):                       # diagonal navy -> deep blue -> brand blue
        for x in range(0, W, 2):
            t = min(1.0, max(0.0, (x / W) * 0.72 + (y / H) * 0.42))
            if t < 0.55:
                u = t / 0.55
                c = tuple(int(NAVY[i] + (DEEP[i] - NAVY[i]) * u) for i in range(3))
            else:
                u = (t - 0.55) / 0.45
                c = tuple(int(DEEP[i] + (BLUE[i] - DEEP[i]) * u * 0.85) for i in range(3))
            px[x, y] = c; px[x + 1, y] = c; px[x, y + 1] = c; px[x + 1, y + 1] = c
    im = im.convert('RGBA')
    blobs = _layer()
    d = ImageDraw.Draw(blobs)
    for colour, alpha in ((SKY, 120), (MINT, 80), (BLUE, 150)):
        cx = rng.uniform(0.52, 0.98) * W
        cy = rng.uniform(0.05, 0.95) * H
        rad = rng.uniform(0.18, 0.34) * W
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=colour + (alpha,))
    im.alpha_composite(blobs.filter(ImageFilter.GaussianBlur(110 * S)))
    grid = _layer()                                 # faint dot grid for texture
    g = ImageDraw.Draw(grid)
    step = 34 * S
    for gy in range(step, H, step):
        for gx in range(int(W * 0.5), W, step):
            g.ellipse([gx - S, gy - S, gx + S, gy + S], fill=(255, 255, 255, 26))
    im.alpha_composite(grid)
    return im


# ------------------------------------------------------------------ motifs ----
# Each motif draws onto a transparent 760x560 (x S) tile; the tile is then tilted
# and pasted on the right side of the cover.
TW, TH = 760 * S, 560 * S


def _tile():
    from PIL import Image
    return Image.new('RGBA', (TW, TH), (0, 0, 0, 0))


def _card(t, box, r=26, fill=(255, 255, 255, 40), outline=(255, 255, 255, 110)):
    from PIL import ImageDraw
    lay = _tile()
    _rr(ImageDraw.Draw(lay), [v * S for v in box], r * S, fill=fill, outline=outline, width=2 * S)
    t.alpha_composite(lay)


def _bar(d, box, colour, r=8):
    _rr(d, [v * S for v in box], r * S, fill=colour)


def m_browser(t, rng, accent):
    from PIL import ImageDraw
    _card(t, (40, 40, 720, 520))
    d = ImageDraw.Draw(t)
    for i, c in enumerate(((255, 110, 110), (255, 200, 90), (110, 230, 150))):
        d.ellipse([(70 + i * 34) * S, 66 * S, (92 + i * 34) * S, 88 * S], fill=c + (255,))
    _bar(d, (190, 62, 600, 94), (255, 255, 255, 60), 16)
    _bar(d, (70, 130, 400, 168), (255, 255, 255, 235), 10)       # headline
    _bar(d, (70, 184, 340, 206), (255, 255, 255, 120))
    _bar(d, (70, 220, 370, 242), (255, 255, 255, 120))
    _bar(d, (70, 274, 230, 324), accent + (255,), 25)            # button
    _card(t, (440, 130, 690, 330), 20, fill=accent + (90,), outline=(255, 255, 255, 150))
    d.polygon([(470 * S, 310 * S), (540 * S, 220 * S), (590 * S, 270 * S), (630 * S, 235 * S), (670 * S, 310 * S)], fill=(255, 255, 255, 200))
    d.ellipse([610 * S, 160 * S, 650 * S, 200 * S], fill=AMBER + (255,))
    for i in range(3):                                           # feature cards
        x = 70 + i * 215
        _card(t, (x, 370, x + 190, 490), 16, fill=(255, 255, 255, 46))
        d.ellipse([(x + 18) * S, 390 * S, (x + 54) * S, 426 * S], fill=(accent if i == 1 else SKY) + (255,))
        _bar(d, (x + 18, 440, x + 150, 454), (255, 255, 255, 170), 6)
        _bar(d, (x + 18, 464, x + 110, 476), (255, 255, 255, 100), 6)


def m_chart(t, rng, accent):
    from PIL import ImageDraw
    _card(t, (40, 60, 720, 500))
    d = ImageDraw.Draw(t)
    _bar(d, (76, 92, 300, 122), (255, 255, 255, 230), 8)
    _bar(d, (76, 136, 220, 154), (255, 255, 255, 110), 6)
    heights = [90, 130, 115, 175, 215, 265]
    pts = []
    for i, h in enumerate(heights):
        x = 90 + i * 100
        col = (accent if i == len(heights) - 1 else SKY) + (255 if i == len(heights) - 1 else 190,)
        _rr(d, [x * S, (450 - h) * S, (x + 58) * S, 450 * S], 12 * S, fill=col)
        pts.append(((x + 29) * S, (450 - h - 34) * S))
    d.line(pts, fill=(255, 255, 255, 240), width=5 * S, joint='curve')
    for p in pts:
        d.ellipse([p[0] - 9 * S, p[1] - 9 * S, p[0] + 9 * S, p[1] + 9 * S], fill=(255, 255, 255, 255))
    _card(t, (500, 20, 740, 130), 22, fill=(255, 255, 255, 235), outline=(255, 255, 255, 255))   # KPI chip
    d.polygon([(532 * S, 96 * S), (560 * S, 54 * S), (588 * S, 96 * S)], fill=(22, 163, 74, 255))
    _bar(d, (606, 52, 712, 72), DEEP + (255,), 6)
    _bar(d, (606, 84, 680, 98), (120, 140, 160, 255), 6)


def m_flow(t, rng, accent):
    from PIL import ImageDraw
    d = ImageDraw.Draw(t)
    nodes = [(60, 60, 280, 170), (60, 380, 280, 490), (480, 60, 700, 170), (480, 380, 700, 490)]
    centre = (380, 275)
    for (x0, y0, x1, y1) in nodes:
        d.line([((x0 + x1) // 2 * S, (y0 + y1) // 2 * S), (centre[0] * S, centre[1] * S)], fill=(255, 255, 255, 150), width=4 * S)
    for i, (x0, y0, x1, y1) in enumerate(nodes):
        _card(t, (x0, y0, x1, y1), 22)
        d.ellipse([(x0 + 22) * S, (y0 + 30) * S, (x0 + 72) * S, (y0 + 80) * S], fill=((SKY, MINT, AMBER, PINK)[i]) + (255,))
        _bar(d, (x0 + 90, y0 + 36, x1 - 24, y0 + 52), (255, 255, 255, 220), 6)
        _bar(d, (x0 + 90, y0 + 64, x1 - 60, y0 + 76), (255, 255, 255, 110), 6)
    r = 92
    glow = _tile()
    ImageDraw.Draw(glow).ellipse([(centre[0] - r - 26) * S, (centre[1] - r - 26) * S, (centre[0] + r + 26) * S, (centre[1] + r + 26) * S], fill=accent + (70,))
    t.alpha_composite(glow)
    d.ellipse([(centre[0] - r) * S, (centre[1] - r) * S, (centre[0] + r) * S, (centre[1] + r) * S], fill=(255, 255, 255, 245))
    # four-point spark = "AI"
    cx, cy = centre[0] * S, centre[1] * S
    for big, off in ((58, (0, 0)), (22, (52, -46))):
        b = big * S; ox, oy = off[0] * S, off[1] * S; n = b * 0.26
        d.polygon([(cx + ox, cy + oy - b), (cx + ox + n, cy + oy - n), (cx + ox + b, cy + oy), (cx + ox + n, cy + oy + n),
                   (cx + ox, cy + oy + b), (cx + ox - n, cy + oy + n), (cx + ox - b, cy + oy), (cx + ox - n, cy + oy - n)], fill=accent + (255,))


def m_video(t, rng, accent):
    from PIL import ImageDraw
    _card(t, (40, 70, 720, 450), 30, fill=(255, 255, 255, 44))
    d = ImageDraw.Draw(t)
    _rr(d, [70 * S, 100 * S, 690 * S, 372 * S], 20 * S, fill=accent + (120,))
    d.polygon([(70 * S, 372 * S), (250 * S, 220 * S), (360 * S, 310 * S), (470 * S, 190 * S), (690 * S, 372 * S)], fill=(255, 255, 255, 70))
    d.ellipse([560 * S, 130 * S, 630 * S, 200 * S], fill=AMBER + (255,))
    cx, cy, r = 380 * S, 236 * S, 66 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 250))
    d.polygon([(cx - 20 * S, cy - 32 * S), (cx - 20 * S, cy + 32 * S), (cx + 36 * S, cy)], fill=DEEP + (255,))
    _bar(d, (70, 398, 690, 410), (255, 255, 255, 80), 6)       # scrubber
    _bar(d, (70, 398, 330, 410), (255, 255, 255, 250), 6)
    d.ellipse([318 * S, 390 * S, 346 * S, 418 * S], fill=(255, 255, 255, 255))
    for i in range(4):                                          # filmstrip
        x = 70 + i * 160
        _card(t, (x, 472, x + 140, 546), 12, fill=((SKY, MINT, AMBER, PINK)[i]) + (150,), outline=(255, 255, 255, 170))


def m_phone(t, rng, accent):
    from PIL import ImageDraw
    d = ImageDraw.Draw(t)
    _card(t, (70, 20, 330, 540), 44, fill=(255, 255, 255, 52))
    _bar(d, (160, 42, 240, 56), (255, 255, 255, 140), 7)
    d.ellipse([150 * S, 110 * S, 250 * S, 210 * S], fill=accent + (255,))
    d.ellipse([178 * S, 132 * S, 222 * S, 176 * S], fill=(255, 255, 255, 255))
    d.pieslice([160 * S, 170 * S, 240 * S, 250 * S], 180, 360, fill=(255, 255, 255, 255))
    _bar(d, (120, 236, 280, 254), (255, 255, 255, 230), 8)
    _bar(d, (146, 268, 254, 282), (255, 255, 255, 120), 6)
    d.ellipse([110 * S, 420 * S, 180 * S, 490 * S], fill=(239, 68, 68, 255))
    d.ellipse([220 * S, 420 * S, 290 * S, 490 * S], fill=(34, 197, 94, 255))
    _card(t, (370, 90, 740, 250), 26, fill=(255, 255, 255, 240), outline=(255, 255, 255, 255))   # speech bubble
    hs = [18, 40, 64, 30, 78, 52, 24, 60, 36, 70, 28, 46, 20]
    for i, h in enumerate(hs):
        x = 398 + i * 25
        _rr(d, [x * S, (170 - h // 2) * S, (x + 12) * S, (170 + h // 2) * S], 6 * S, fill=(accent if i % 3 else DEEP) + (255,))
    _card(t, (430, 300, 740, 420), 24)
    d.ellipse([452 * S, 326 * S, 520 * S, 394 * S], fill=MINT + (255,))
    d.line([(470 * S, 362 * S), (483 * S, 376 * S), (504 * S, 346 * S)], fill=DEEP + (255,), width=7 * S)
    _bar(d, (540, 338, 710, 356), (255, 255, 255, 230), 7)
    _bar(d, (540, 370, 660, 384), (255, 255, 255, 120), 6)


def m_shop(t, rng, accent):
    from PIL import ImageDraw
    d = ImageDraw.Draw(t)
    _card(t, (40, 150, 720, 530))
    cols = (PINK, (255, 255, 255), SKY, (255, 255, 255), MINT, (255, 255, 255), AMBER)   # awning
    for i, c in enumerate(cols):
        x0 = 30 + i * 100
        d.pieslice([x0 * S, 80 * S, (x0 + 100) * S, 200 * S], 0, 180, fill=c + (250,))
        d.rectangle([x0 * S, 60 * S, (x0 + 100) * S, 140 * S], fill=c + (250,))
    for i in range(3):
        x = 70 + i * 215
        _card(t, (x, 230, x + 190, 430), 18, fill=(255, 255, 255, 235), outline=(255, 255, 255, 255))
        c = (accent, SKY, AMBER)[i]
        _rr(d, [(x + 20) * S, 250 * S, (x + 170) * S, 350 * S], 14 * S, fill=c + (200,))
        _bar(d, (x + 20, 366, x + 150, 382), DEEP + (255,), 6)
        _bar(d, (x + 20, 394, x + 90, 410), (22, 163, 74, 255), 6)
    _rr(d, [250 * S, 452 * S, 510 * S, 506 * S], 27 * S, fill=accent + (255,))
    _bar(d, (310, 472, 450, 486), (255, 255, 255, 255), 6)


def m_news(t, rng, accent):
    from PIL import ImageDraw
    d = ImageDraw.Draw(t)
    for k, (dx, dy, a) in enumerate(((60, 0, 26), (30, 30, 34), (0, 60, 48))):
        _card(t, (40 + dx, 30 + dy, 660 + dx, 440 + dy), 26, fill=(255, 255, 255, a))
    _rr(d, [72 * S, 124 * S, 232 * S, 160 * S], 18 * S, fill=accent + (255,))
    _bar(d, (72, 184, 560, 220), (255, 255, 255, 240), 10)
    _bar(d, (72, 236, 470, 272), (255, 255, 255, 240), 10)
    for i in range(4):
        _bar(d, (72, 306 + i * 34, 600 - (i % 2) * 110, 322 + i * 34), (255, 255, 255, 120), 7)
    cx, cy = 640 * S, 470 * S
    d.ellipse([cx - 60 * S, cy - 60 * S, cx + 60 * S, cy + 60 * S], fill=(255, 255, 255, 245))
    for i, rr_ in enumerate((18, 34, 50)):
        d.arc([cx - rr_ * S, cy - rr_ * S, cx + rr_ * S, cy + rr_ * S], 300, 60, fill=(accent if i < 2 else DEEP) + (255,), width=6 * S)
    d.ellipse([cx - 9 * S, cy - 9 * S, cx + 9 * S, cy + 9 * S], fill=DEEP + (255,))


def m_shield(t, rng, accent):
    from PIL import ImageDraw
    d = ImageDraw.Draw(t)
    _card(t, (330, 60, 730, 500))
    for i in range(4):
        y = 110 + i * 92
        col = MINT if i < 3 else AMBER
        d.ellipse([366 * S, y * S, 414 * S, (y + 48) * S], fill=col + (255,))
        if i < 3:
            d.line([(378 * S, (y + 25) * S), (388 * S, (y + 35) * S), (403 * S, (y + 14) * S)], fill=DEEP + (255,), width=6 * S)
        _bar(d, (436, y + 6, 690 - (i % 2) * 60, y + 22), (255, 255, 255, 225), 7)
        _bar(d, (436, y + 32, 610, y + 44), (255, 255, 255, 110), 6)
    cx, top = 190 * S, 110 * S
    sh = [(cx, top), (cx + 140 * S, top + 44 * S), (cx + 140 * S, top + 190 * S), (cx, top + 350 * S), (cx - 140 * S, top + 190 * S), (cx - 140 * S, top + 44 * S)]
    d.polygon(sh, fill=(255, 255, 255, 245))
    inner = [(cx, top + 34 * S), (cx + 108 * S, top + 68 * S), (cx + 108 * S, top + 180 * S), (cx, top + 306 * S), (cx - 108 * S, top + 180 * S), (cx - 108 * S, top + 68 * S)]
    d.polygon(inner, fill=accent + (255,))
    d.line([(cx - 52 * S, top + 170 * S), (cx - 12 * S, top + 212 * S), (cx + 58 * S, top + 118 * S)], fill=(255, 255, 255, 255), width=18 * S, joint='curve')


def m_course(t, rng, accent):
    from PIL import ImageDraw
    d = ImageDraw.Draw(t)
    for i in range(4):                                   # lesson cards, stepped
        x, y = 60 + i * 60, 330 - i * 78
        _card(t, (x, y, x + 440, y + 150), 22, fill=(255, 255, 255, 60 + i * 55 if i < 3 else 240), outline=(255, 255, 255, 200))
        col = (SKY, MINT, AMBER, accent)[i]
        d.ellipse([(x + 24) * S, (y + 30) * S, (x + 100) * S, (y + 106) * S], fill=col + (255,))
        ink = DEEP if i == 3 else (255, 255, 255)
        _bar(d, (x + 124, y + 40, x + 380, y + 62), ink + (255 if i == 3 else 220,), 8)
        _bar(d, (x + 124, y + 78, x + 300, y + 94), (ink if i < 3 else (110, 130, 150)) + (130 if i < 3 else 255,), 6)
    x, y = 240, 96                                       # play triangle on top card
    d.polygon([((x + 52) * S, (y + 50) * S), ((x + 52) * S, (y + 86) * S), ((x + 82) * S, (y + 68) * S)], fill=(255, 255, 255, 255))
    cx, cy = 610 * S, 400 * S                            # graduation cap
    d.polygon([(cx, cy - 60 * S), (cx + 120 * S, cy - 10 * S), (cx, cy + 40 * S), (cx - 120 * S, cy - 10 * S)], fill=(255, 255, 255, 250))
    d.polygon([(cx - 66 * S, cy + 20 * S), (cx + 66 * S, cy + 20 * S), (cx + 66 * S, cy + 70 * S), (cx, cy + 100 * S), (cx - 66 * S, cy + 70 * S)], fill=(255, 255, 255, 200))
    d.line([(cx + 100 * S, cy - 4 * S), (cx + 100 * S, cy + 70 * S)], fill=AMBER + (255,), width=6 * S)
    d.ellipse([cx + 88 * S, cy + 62 * S, cx + 112 * S, cy + 86 * S], fill=AMBER + (255,))


DRAW = {'browser': m_browser, 'chart': m_chart, 'flow': m_flow, 'video': m_video, 'phone': m_phone,
        'shop': m_shop, 'news': m_news, 'shield': m_shield, 'course': m_course}


def _wrap(draw, text, font, max_w):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def human_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return '%s %d, %d' % (d.strftime('%B'), d.day, d.year)


PHOTO_DIR = os.path.join(HERE, '_photos')     # 1600x900 master photos, one per post slug (underscore = not served)


def photo_key(slug):
    return slug.replace('/', '--')


def photo_for(slug):
    for ext in ('.jpg', '.jpeg', '.png', '.webp'):
        p = os.path.join(PHOTO_DIR, photo_key(slug) + ext)
        if os.path.exists(p):
            return p
    return None


def fit(im, w, h):
    """Centre-crop to w:h, then resize."""
    from PIL import Image
    im = im.convert('RGB')
    r = w / h
    if im.width / im.height > r:
        nw = int(im.height * r); x = (im.width - nw) // 2
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / r); y = (im.height - nh) // 2
        im = im.crop((0, y, im.width, y + nh))
    return im.resize((w, h), Image.LANCZOS)


def make_photo_cover(photo_path, out_path):
    """1200x630 cover from a photo: clean image, soft bottom shade, small site tag. No title text
    (the page prints the title above the picture)."""
    from PIL import Image, ImageDraw
    im = fit(Image.open(photo_path), 1200, 630).convert('RGBA')
    shade = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for y in range(470, 630):
        d.line([(0, y), (1200, y)], fill=(6, 20, 44, int(150 * ((y - 470) / 160) ** 1.6)))
    im.alpha_composite(shade)
    d = ImageDraw.Draw(im)
    d.text((40, 582), 'novatoronto.com', font=_font(F_SEMI, 24), fill=(255, 255, 255, 235))
    d.rectangle([0, 622, 1200, 630], fill=(255, 255, 255, 255))
    d.rectangle([0, 622, 384, 630], fill=SKY + (255,))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.convert('RGB').save(out_path, 'JPEG', quality=86, optimize=True, progressive=True)
    return os.path.getsize(out_path)


def make_cover(post, date_iso, out_path, motif=None):
    from PIL import Image, ImageDraw, ImageFilter
    slug = post.get('slug', 'post')
    if motif is None and photo_for(slug):          # a real photo beats the drawn cover
        return make_photo_cover(photo_for(slug), out_path)
    seed = int(hashlib.sha256(slug.encode('utf-8')).hexdigest()[:8], 16)
    rng = random.Random(seed)
    motif = motif or pick_motif(slug, post.get('category', ''))
    accent = (BLUE, (56, 189, 248), (20, 184, 166), (99, 102, 241))[seed % 4]

    im = _background(rng)

    # --- illustration (right)
    tile = _tile()
    DRAW[motif](tile, rng, accent)
    angle = rng.choice([-7, -5, -4, 4, 5, 7])
    shadow = Image.new('RGBA', tile.size, (0, 0, 0, 0))
    shadow.paste((2, 10, 28, 110), mask=tile.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(22 * S))
    scale = 0.80                                     # keep the art clear of the title column
    for lay, off in ((shadow, (12 * S, 22 * S)), (tile, (0, 0))):
        small = lay.resize((int(TW * scale), int(TH * scale)), Image.LANCZOS)
        rot = small.rotate(angle, resample=Image.BICUBIC, expand=True)
        x = 578 * S + (int(TW * scale) - rot.width) // 2 + off[0]
        y = (H - rot.height) // 2 + 4 * S + off[1]
        im.alpha_composite(rot, (x, y))

    # --- left text scrim so the title always reads
    scrim = _layer()
    sd = ImageDraw.Draw(scrim)
    for x in range(0, int(W * 0.56), 4):
        a = int(215 * (1 - x / (W * 0.56)) ** 1.4)
        sd.rectangle([x, 0, x + 4, H], fill=NAVY + (a,))
    im.alpha_composite(scrim)

    d = ImageDraw.Draw(im)
    x0, y = 70 * S, 56 * S
    logo_p = os.path.join(REPO, 'assets', 'img', 'NovaToronto.png')
    if os.path.exists(logo_p):
        logo = Image.open(logo_p).convert('RGBA')
        lw = 168 * S
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        px = logo.load()
        for yy in range(logo.height):                    # dark ink -> white, keep the blue accents
            for xx in range(logo.width):
                r, g, b, a = px[xx, yy]
                if a and r < 110 and g < 110 and b < 110:
                    px[xx, yy] = (255, 255, 255, a)
        im.alpha_composite(logo, (x0, y))
        y += logo.height + 22 * S

    # category pill + date
    f_pill = _font(F_BOLD, 21 * S)
    label = post.get('category', 'Nova Toronto').upper()
    pw = int(d.textlength(label, font=f_pill)) + 40 * S
    _rr(d, (x0, y, x0 + pw, y + 44 * S), 22 * S, fill=(255, 255, 255, 255))
    d.text((x0 + 20 * S, y + 8 * S), label, font=f_pill, fill=DEEP)
    f_date = _font(F_SEMI, 21 * S)
    d.text((x0 + pw + 18 * S, y + 8 * S), human_date(date_iso), font=f_date, fill=(205, 228, 245))
    y += 44 * S + 30 * S

    # title: biggest size that fits 3 lines in the left column
    title = post.get('cover_title') or post.get('title', '')
    max_w = 505 * S
    for size, max_lines in ((66, 3), (60, 3), (54, 3), (50, 4), (46, 4), (42, 4), (38, 5)):
        f_h = _font(F_BOLD, size * S)
        lines = _wrap(d, title, f_h, max_w)
        if len(lines) <= max_lines:
            break
    lh = int(size * S * 1.14)
    for line in lines[:5]:
        d.text((x0 + 3 * S, y + 3 * S), line, font=f_h, fill=(2, 14, 34))
        d.text((x0, y), line, font=f_h, fill=(255, 255, 255))
        y += lh
    y += 18 * S
    d.rectangle([x0, y, x0 + 84 * S, y + 6 * S], fill=accent if accent != BLUE else SKY)
    y += 26 * S
    d.text((x0, y), 'By Rujal Tuladhar  ·  novatoronto.com', font=_font(F_SEMI, 24 * S), fill=(214, 233, 247))

    d.rectangle([0, H - 12 * S, W, H], fill=(255, 255, 255))
    d.rectangle([0, H - 12 * S, int(W * 0.32), H], fill=SKY)

    out = im.convert('RGB').resize((1200, 630), Image.LANCZOS)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out.save(out_path, 'JPEG', quality=88, optimize=True, progressive=True)
    return os.path.getsize(out_path)


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, '_cover_samples')
    samples = [
        ('browser', 'how-much-does-a-website-cost-toronto-2026', 'Website Design', 'What a Website Costs in Toronto in 2026'),
        ('chart', 'google-ads-vs-meta-ads-ontario', 'Digital Marketing', 'Google Ads vs Meta Ads for Ontario Shops'),
        ('flow', 'automate-quotes-with-ai', 'AI Automation', 'Automate Your Quotes With AI'),
        ('video', 'ai-video-ad-cost-canada', 'AI Tools', 'What an AI Video Ad Costs'),
        ('phone', 'ai-receptionist-vs-answering-service', 'AI Automation', 'AI Receptionist vs Answering Service'),
        ('shop', 'shopify-vs-woocommerce-canada', 'Website Design', 'Shopify vs WooCommerce in Canada'),
        ('news', 'ai-news-for-business-october-2026', 'AI News', 'AI This Week: October 2, 2026'),
        ('shield', 'casl-rules-email-marketing-ontario', 'Digital Marketing', 'CASL Rules for Email Marketing'),
        ('course', 'free-ai-course-for-beginners', 'AI Tools', 'Free AI Course for Beginners'),
    ]
    for motif, slug, cat, title in samples:
        p = os.path.join(out_dir, motif + '.jpg')
        kb = make_cover({'slug': slug, 'category': cat, 'cover_title': title}, '2026-10-02', p) // 1024
        print('%-8s %-45s -> %s (%d KB)' % (pick_motif(slug, cat), slug, p, kb))
