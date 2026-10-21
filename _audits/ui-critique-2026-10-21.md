# UI design critique: novatoronto.com homepage (2026-10-21)

Checked at phone size (375×812) and desktop (1280–1366 wide) on a local copy, using automated checks (contrast, tap
sizes, alt text, button and heading styles, call-to-action wording) plus screenshots of each section.

## Overall impression
The top of the page is now strong: the slider makes a clear offer with a button, and the bakery video gives the brand
personality. The biggest remaining problem is the long middle of the page. Visitors have to scroll past free tools and
two AI-video sections before they see what you sell, what it costs and how to contact you. Floating buttons also
cover part of every section on phones.

## Usability
| Finding | Severity | Recommendation |
|---|---|---|
| The page is ~32 phone screens long; "What We Do" starts at screen ~8, pricing at ~23, the contact form at ~28 | 🔴 Critical | Reorder: Hero → What We Do → Portfolio → How AI works → Pricing → Contact; then the free AI toolkit, AI video (merged), blog, areas |
| Two floating buttons ("Talk to Nova" pill plus the Call Now / Book Free Call bar) cover ~20% of every phone screen, including text and videos | 🔴 Critical | On phones, put "Talk to Nova" inside the bottom bar as a third icon button, or show it only after 50% scroll; keep one floating element |
| 16 different wordings for the main call to action ("Book Free Call", "Book My Free Consultation", "Book a Free 20-min Call", "Book a free 15-min call", "Get Started" ×3, "Schedule Now"…) and both **15-min and 20-min** promised | 🟡 Moderate | Pick one offer and one label site-wide, e.g. "Book a free 15-min call", in the slider, hero, sections, bottom bar and the video end card |
| Contact hours "7–10 AM & 8–11 PM EST" and "Call **Me**" read like a side business; most of the site says "we" | 🟡 Moderate | Show "Mon–Sat, 9 AM–9 PM" (the AI receptionist covers the gaps), or "Calls answered 24/7 by our AI receptionist"; use "we" consistently |
| No testimonials or review stars anywhere on the page | 🟡 Moderate | Add 2–3 real client quotes (Do Home Healthcare, Tawa Grill, IGR Logistics) with name and business, near the portfolio |
| The mobile menu has 12 links (6 service sub-links) in mixed case (HOME vs Website Design) | 🟢 Minor | Group services under one "Services ▾" item; use one letter case |
| Hero copy under "Schedule Now" reads like an internal note: "Captures the full journey you enable…" | 🟡 Moderate | "We build your website, bring in traffic, automate the busywork and turn visitors into paying customers." |

## Visual hierarchy
- **What draws the eye first:** the slider headline and blue button. Correct: it states an outcome and gives one clear action.
- **Reading flow:** slider → H1 → "From Click to Customer" → video. The H1 repeats what the slider already says, so on
  phones it pushes the video down without adding much. Consider shrinking it further or moving it below the video.
- **Emphasis:** in the long sections (free AI prompts, AI video) every card has equal weight, so nothing stands out.
  The pricing section opens with ROAS/tROAS jargon instead of the website price most visitors are looking for.

## Consistency
| Element | Issue | Recommendation |
|---|---|---|
| Section headings | All 28px title case, except "WEBSITE DESIGNS" (all caps) and the subscribe heading (24px) | Title case for all: "Website Designs" or better "Our Work" |
| Buttons | 3 font sizes (16 / 14 / 13.3px), filled and outline styles mixed for the same action | One primary (filled #0073a8, 16px) and one secondary (outline) style |
| Copy | "We may not have met yet, but **here** some of our work." | "…but here's some of our work." |
| Text colours | 14 different text colours in sections | Limit to title, body, muted and link/brand |

## Accessibility
- **Colour contrast:** everything passes AA except the slider buttons (white on #0096dd, 3.3:1). **Fixed in this pass** (now #0073a8, 5.2:1).
- **Touch targets:** 91 links or buttons are under 44px. The worst are the "Read Story" links (17px tall), the industry
  chips (37px) and the inline text links. The slider dots are **fixed** (44px tall).
- **Text readability:** body 16px Inter, headings Poppins. Paragraph line-height varies from "normal" (~1.2) to 1.8;
  standardise at 1.6. "Our AI assistant — live demo" is 10.9px; make it at least 12px.
- **Alt text:** no images are missing alt text. The slider images use empty alt on purpose (the text sits on top of them).

## What works well
- A clear, outcome-led slider with one action per slide, and a fast first image (35 KB).
- The bakery video in the hero gives the brand a human, local feel nobody else in the GTA has.
- The "How AI Automation Works" step cards are scannable and concrete (6:03 PM missed call → AI answers).
- Consistent fonts (Poppins + Inter), card style and brand blue.
- Sticky Call Now / Book Free Call bar: good for mobile conversion. It just needs fewer competing floating buttons.

## Priority recommendations
1. **Reorder the sections** so the offer, proof, price and contact come within the first ~10 phone screens; collapse the free AI prompts to 2 plus "see all".
2. **One floating element on phones:** merge "Talk to Nova" into the bottom bar.
3. **One call to action everywhere** ("Book a free 15-min call") and fix the 15 vs 20 minute conflict.
4. **Add social proof** (2–3 client quotes) next to the portfolio.
5. **Copy cleanup:** hero description, "here's", "WEBSITE DESIGNS", contact hours and "we" voice.
