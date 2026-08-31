# Thresholds and what they mean

Pass/fail lines for the probe output, and — more importantly — why a visitor cares.
Cite the number *and* the consequence; a threshold with no consequence attached is
just trivia.

## Contrast (WCAG 2.1)

| Text | Minimum (AA) | Comfortable (AAA) |
|---|---|---|
| Body, under 18.66px | **4.5:1** | 7:1 |
| Large: 24px+, or 18.66px+ bold | **3:1** | 4.5:1 |
| Icons, form borders, focus rings | **3:1** | — |

Below 4.5:1, body text becomes hard to read on a phone outdoors, on a cheap laptop
panel, or for anyone over about 40. Placeholder grey and "muted" caption colours are
the usual offenders — they look elegant on a calibrated monitor in a dim room and
vanish everywhere else.

The probe reports `severity: severe` when a ratio is below 70% of what it needs.
Severe failures on body copy or CTAs are Critical; marginal failures on footer
microcopy are Minor.

## Tap targets

**44×44px minimum** (Apple HIG; WCAG 2.5.5 says 44, Android says 48).

Anything smaller gets mis-tapped on a phone. Weight by what the element does: a
mis-tapped nav icon is an annoyance, a mis-tapped *Submit* or phone-number link is a
lost lead. Inline text links inside a paragraph are exempt — they're understood as
text, not buttons.

## Typography

- **Line length: 45–75 characters.** Past ~85 the eye loses its place returning to
  the next line; under ~30 the text feels choppy and column-like. The probe reports
  outliers in both directions.
- **Distinct font sizes: aim for 6–9.** More than about 12 means there's no scale,
  just accumulated one-offs, and nothing reads as reliably more important than
  anything else.
- **Body text: 16px minimum.** Below 14px is a red flag on mobile; iOS also zooms
  form inputs under 16px on focus, which feels broken.
- **Font families: 1–2.** A third family is almost always an accident.

## Spacing

More than ~12 distinct margin/padding values across sections means spacing is
ad-hoc rather than a scale. The visible symptom is that sections feel arbitrarily
crammed or loose relative to each other, which reads as unpolished even to people
who can't name why.

Look for whether the most-used values form a recognisable progression (8/16/24/32,
or a `rem` scale). A long tail of single-use values is the drift signal.

## Design-system drift

`tokens.hardcodedHexInStyleBlocks` vs `tokens.declaredTokens` is the tell. A site
with a proper token system should reference `var(--first-color)`, not repeat
`#0096DD` in twelve places — because the day the brand colour changes, every
hardcoded copy is a bug.

Some hardcoding is legitimate: pure black video letterboxing, shadow rgba values.
Judge whether the value is *semantic* (a brand colour, a surface, a text colour →
should be a token) or *incidental*.

`inlineStyleAttrs` in the hundreds means styling decisions live in markup where
they can't be reused or themed.

## Heading order

- Exactly **one `h1`** per page.
- **No level skips** (h2 → h4). Screen-reader users navigate by heading level;
  a skip reads as a missing section.
- Headings should describe content, not styling. An `h3` chosen because it "looked
  the right size" is a hierarchy bug.

## Focus states

`focusRuleCount: 0` is a hard failure — keyboard and switch users literally cannot
see where they are. Browsers' default focus ring is often removed by CSS resets
without a replacement, which is the most common way this happens.

Prefer `:focus-visible` over `:focus` so mouse users don't see rings on click.

## Performance (perceived)

| Metric | Good | Concerning |
|---|---|---|
| Total transfer, first view | under 1.5 MB | over 3 MB |
| Single asset | under 300 KB | over 1 MB |
| DOMContentLoaded | under 1.5 s | over 3 s |
| Images oversized vs render size | ≤2× | >2.5× |

`oversized` images are free wins — serving a 1920px image into a 300px slot wastes
the visitor's data and delays paint for zero visual benefit.

Above-the-fold weight matters more than total. A heavy asset below the fold that is
`preload="none"` or lazy-loaded costs nothing until it's needed.

## Above-the-fold CTAs

More than about **2 competing calls to action** and each one gets weaker — the
visitor has to make a choice before they understand the offer, so many make none.
Count distinct *destinations*, not buttons: three buttons all pointing at `#contact`
are one CTA repeated, which is fine and often good.

## Ranking findings

Rank by expected effect on the conversion goal, roughly:

1. **Blocks or hides conversion** — form broken, CTA invisible, page overflows on
   mobile, contact info unreadable
2. **Erodes trust before conversion** — visible layout breakage, unreadable body
   copy, obviously broken images
3. **Adds friction** — small tap targets, long line lengths, slow above-fold load
4. **Accumulating debt** — token drift, spacing inconsistency, heading order
5. **Taste** — label it as taste and put it last

A severe contrast failure on a footer link outranks nothing. A marginal one on the
primary CTA outranks almost everything.
