# Design Audit — novatoronto.com — 2026-08-30

**Audited:** homepage, live site, at 1280×900 and 375×812
**Conversion goal:** form submissions and phone calls from GTA small businesses
**Method:** measured with `design-audit` skill probe (373 text nodes, 25 images,
145 interactive elements), cross-checked against source

---

## Verdict

The design itself is not the problem — the palette is coherent, typography is
disciplined (one family, sensible scale), and there is no layout breakage at any
width. The problem is that **the two things a local service business converts on
are both broken or buried**: the phone number is not tappable anywhere on the
site, and the contact form sits 88% of the way down a page that is 21,395px tall.

If you fix one thing, make the phone number a `tel:` link. It is a ten-minute
change and it is the single clearest lost-lead path on the site.

---

## Critical — costing conversions now

### 1. The phone number is not a link. Anywhere. On any page.

- **Measured:** `0` elements matching `a[href^="tel:"]` across all ~60 HTML pages.
  The number appears as plain text inside a `<span>`, and on only **2 of ~60 pages**.
- **Where:** `index.html:2363` — `<span class="contact__subtitle">365-355-3133</span>`
- **Why it costs you:** Most of your traffic is mobile, and most local-service
  buyers call rather than fill in a form. A visitor sees the number, taps it,
  nothing happens, and they go back to Google. Every one of those is a lost lead
  from a visitor who had already decided to contact you.
- **Fix:** `<a href="tel:+13653553133" class="contact__subtitle">365-355-3133</a>`,
  and add the number to the header and footer site-wide so it is reachable from
  every page — not just two.

### 2. The contact form is 26 phone-screens down

- **Measured:** `#contact` starts at **18,746px** on a **21,395px** page = **88% down**.
  At 812px of phone viewport that is roughly 23 full swipes.
- **Where:** `index.html` — `#contact` is the second-to-last section
- **Why it costs you:** Nobody scrolls 88% of a page. The CTA buttons that jump to
  `#contact` help, but only for people who notice them. There is no persistent way
  to convert while reading.
- **Fix:** Add a sticky mobile call/book bar (the "Talk to Nova" widget already
  proves the pattern works). Cheapest version: a fixed bottom bar under 768px with
  two buttons — *Call* (`tel:`) and *Book*  (`#contact`).

### 3. The primary CTA fails contrast — and so does every blue link on the site

- **Measured:** "Schedule Now", white on `rgb(0,146,214)` = **3.45:1**. WCAG AA needs
  **4.5:1** for 16px non-bold text. The same 3.45:1 appears on 8 separate elements
  because it is the brand blue itself against white.
- **Where:** `index.html` `#hero-call-btn`; also `.svc__price`, `.aic__badge`,
  `.aic__proof-link`, `.pg__link`, `.nav__link.active-link`, the Nova widget subtext
- **Why it costs you:** The button you most want tapped is the hardest to read —
  on a phone outdoors, on a cheap laptop panel, or for anyone over 40. You sell web
  design; a prospect who checks your accessibility will find it here first.
- **Fix:** Darken the brand blue one step for *text and button fills only*, leaving
  decorative use as-is: `hsl(199, 100%, 34%)` ≈ `#0075AB` gives **4.6:1** on white
  and reads as the same colour. Set it as a token (e.g. `--first-color-text`) so it
  applies everywhere at once.
- **Worst single case:** `h3` "With AI automation" at **3.09:1** — blue on a pale
  blue tint in the AI-automation infographic.

---

## Important — credibility and polish

### 4. Above-the-fold images are enormous

| File | Weight | Natural | Rendered |
|---|---:|---|---|
| `toronto-travel_2x3.png` | **2,254 KB** | 1534×2302 | 336px wide |
| `Nova_toronto_mobile.gif` | 790 KB | 2025×1350 | mobile hero |
| `colorsoft_for_rujal.png` | 1,455 KB | 1489×1076 | 338px wide |
| `promax_agency.png` | 866 KB | 1024×613 | 338px wide |

- **Why it costs you:** The hero image is ~7× larger than the slot it renders into.
  On mobile data that is the delay before anyone sees anything.
- **Fix:** Resize to ~2× the rendered width and re-encode. `toronto-travel_2x3.png`
  at 700px wide would drop from 2,254 KB to well under 200 KB with no visible change.
  Add `loading="lazy"` to the portfolio images (they are far below the fold).
- **Note:** `Background.png` (7,974 KB) and `IMG_0075.jpg` (2,271 KB) are **not**
  referenced on the homepage — they bloat the repo but cost visitors nothing. The
  `assets/img/` folder totals **28.9 MB** across 37 files.

### 5. The newsletter input makes iOS zoom the page

- **Measured:** `input[name=email]` font-size **13.33px**. iOS Safari auto-zooms any
  focused input under 16px.
- **Why it costs you:** The page jumps and re-scales the moment someone taps the
  field. It reads as broken, on the one interaction you asked for.
- **Fix:** `font-size: 16px` on that input. Purely a mobile-behaviour fix.

### 6. Form fields and service links are below the tap minimum

- **Measured:** form inputs are **36–38px** tall (44px minimum). `.svc__link`
  "Explore …" links measure **269×17px** — 17px of tap height. **104** interactive
  elements are under 44px at 375px width.
- **Fix:** `min-height: 44px` on inputs; add `padding: .5rem 0` to `.svc__link` so
  the tap area covers the row without changing how it looks.

### 7. Keyboard users cannot see where they are

- **Measured:** **4** `:focus`/`:focus-visible` rules for **145** interactive
  elements — and 3 of those 4 were added in the last two sections built.
- **Fix:** One global rule:
  `a:focus-visible, button:focus-visible, input:focus-visible { outline: 3px solid var(--first-color); outline-offset: 3px; }`

### 8. Social icons have no accessible name

- **Measured:** 3 × `a.home__social-icon`, **31×38px**, no text and no `aria-label`.
- **Fix:** Add `aria-label="Facebook"` etc., and pad to 44×44.

---

## Minor — worth doing eventually

- **4 `<h1>` elements on one page** (should be exactly 1), and **3 heading level
  skips** (h1→h3, h2→h4, h1→h4). Affects screen-reader navigation and is a small
  SEO signal.
- **24 distinct spacing values** (2, 4, 5, 6, 8, 10, 11, 12, 14, 16, 17, 19, 20, 24,
  28, 32, 36, 40, 42, 48, 56, 64, 72, 75px). The core scale (24/8/4/12/20/32) is
  sound; the odd values (5, 11, 17, 19, 42, 75) are one-off drift.
- **95 inline `style` attributes** and 30 hardcoded hex values across 10 inline
  `<style>` blocks. Mostly benign, but it means a brand-colour change is a
  find-and-replace rather than a token edit.
- **Most images lack `width`/`height`**, which causes layout shift as they load.
- **Line lengths up to 182 characters** on `.section__subtitle` (ideal is 45–75).
  Capping those blocks at `max-width: 60ch` would noticeably improve readability.

---

## What is already working — don't break these

- **No horizontal overflow at any width tested.** Document scroll width is exactly
  375px at mobile. This is genuinely well done and easy to lose in a redesign.
- **Typographic discipline:** one family (Inter) across 367 of 373 text nodes, four
  weights, and a coherent size scale. Better than most agency sites.
- **Every image has an `alt` attribute** — zero missing.
- **Above-the-fold CTA count is correct:** two real actions (*Schedule Now*,
  *Talk to Nova*) plus nav. Not diluted.
- **The token system exists and is mostly respected** — the HSL-driven theme means
  the contrast fix in #3 is a one-line change rather than a hunt.

---

## Suggested order of work

1. `tel:` links site-wide + sticky mobile call bar — **highest lead impact, ~1 hour**
2. Darken brand blue for text/buttons to pass 4.5:1 — **one token, fixes 8 elements**
3. Resize the four oversized images — **~3 MB saved, mechanical**
4. 16px on the email input; 44px min-height on form fields and `.svc__link`
5. Global `:focus-visible` rule
6. Heading order and the one-off spacing values
