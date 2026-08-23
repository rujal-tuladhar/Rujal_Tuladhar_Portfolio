# Nova Toronto — Master Marketing Plan
_Last updated: 2026-08-23 · Owner: Rujal Tuladhar_

This is the strategy document. The other files in `_marketing/` are the
ready-to-paste tactical assets. Nothing in this folder is published to
novatoronto.com (underscore folders are excluded from the site build).

---

## 1. The situation, honestly

**The website is not the problem. Traffic is.**

The form pipeline was tested live on 2026-07-21 — a real submission went
through FormSubmit and redirected correctly, which means enquiries *do*
reach novatoronto.ca@gmail.com. The AI receptionist answers and books.
The site is fast, mobile-first, and structurally sound.

What's missing is people arriving. Specifically:

| Gap | Consequence |
|---|---|
| Site relaunched only weeks ago | Google hasn't ranked the new pages yet (3–6 months is normal) |
| ~~Google Search Console not verified~~ **DONE 2026-08-04** | Verified under novatoronto.ca@gmail.com — rankings/indexing data now flowing |
| ~~GA4 not connected~~ **DONE 2026-08-04** | `G-B064YQYKLC` live on all 62 pages; lead events reporting in |
| No Google Business Profile | Missing the single biggest free local-lead source |
| No classifieds/directory listings | Zero presence where "hire someone now" buyers look |
| No paid ads running | No way to buy traffic while SEO matures |

**Conclusion:** the near-term job is not "build more website." It's
*distribution* — get the existing 60 pages in front of people, and turn on
measurement so we stop guessing.

---

## 2. Positioning

**"From click to customer."** Nova Toronto is the agency that doesn't just
launch and leave. Everything is priced transparently, reported monthly, and
managed against real return.

Service priority (deliberate — this is where the money and the margin are):

| Priority | Service | Pitch | Price anchor |
|---|---|---|---|
| **70%** | Digital marketing & ads | Proven higher ROAS; budget and target ROAS kept in sync; MoM & YoY growth with plain-English reporting; no long-term contracts | Custom monthly; most start $500–$1,500/mo ad spend |
| **20%** | AI automation / AI receptionist | Never miss a call; books appointments 24/7; a fraction of a receptionist's salary — **and we demo it live on our own site** | Custom; setup under ~2 weeks |
| **10%** | Website design | The foundation traffic lands on | $900 / $1,800 / $2,000 / $5,000 |
| — | Amazon & Walmart Seller | Differentiator, few local agencies offer it | From $450 |
| — | **AI Video Production** *(new 2026-08-23)* | Brand videos generated with AI — no crew, no studio, delivered in days. **Live proof on the homepage:** the Do Home Healthcare video we produced runs on the client's own site | **$497 / $897 / $1,497** — bundle onto any site build for $500 |

**Our unfair advantage:** we run our own AI receptionist on our own website.
Prospects can *talk to the product* before they buy. No competitor in the GTA
is doing that. Lead with it.

**Second proof asset (new):** the Do Home Healthcare case study at
`novatoronto.com/#ai-video`. We built the client's website *and* produced their
AI brand video — and the same video is verifiably live on their homepage.
That is a checkable claim, not a portfolio screenshot. Use it in every
outreach message: "here's a client site we built, and the video we made for
them — go look at their homepage."

---

## 3. Assets already built and live

| Asset | Count | Purpose |
|---|---:|---|
| Local landing pages (service × city) | 30 | Capture "website design Mississauga"-type searches |
| AI-receptionist industry pages | 8 | Capture "AI receptionist for dentists"-type searches |
| Service hub + sub-pages | ~9 | Topical authority |
| Blog posts (all bylined + dated) | 8 | Trust, long-tail search, newsletter fuel |
| **Total indexed URLs in sitemap** | **60** | |
| Homepage booking form + newsletter form | 2 | Conversion |
| AI voice receptionist ("Nova") | 1 | Conversion + live product demo |
| AI video case study (Do Home Healthcare) | 1 | Proof of the new AI Video service; verifiable on the client's live site |
| Structured data (LocalBusiness, Service, FAQ, Breadcrumb, BlogPosting) | site-wide | Rich results in Google |
| Lead event tracking in `main.js` | site-wide | Fires on form submit, CTA click, AI call start |

---

## 4. Channel plan (ordered by return, not by effort)

### Tier 1 — Free, fastest payback (do these first)

**1. Google Business Profile** — *highest ROI action available, still not done.*
Local searches and Map Pack results are where "near me" buyers convert. Ready-to-paste
description, categories, and services are in `directories-and-outreach.md`.
After setup: add 10+ photos and collect **5 reviews from past clients** — reviews are
the number-one local ranking factor.

**2. Google Search Console** — verify the domain, submit `sitemap.xml`.
Turns SEO from guesswork into data: what we rank for, what's indexed, what to fix.

**3. Kijiji** — 4 ads written and ready (`kijiji-ads.md`), one per service.
Free, high-intent, and refreshable. Repost/refresh every 3–4 days to stay near the top.

**4. Facebook Marketplace + Toronto business groups** — short versions ready in
`classifieds-facebook-craigslist.md`.

### Tier 2 — Free, compounding

**5. Directories:** Yelp Canada, YellowPages.ca, 411.ca, Alignable — blurbs ready.
**6. B2B directories:** Clutch.co, GoodFirms, UpCity — profile copy ready.
**7. Bark.com/ca** — pay-per-lead, free profile.
**8. Craigslist Toronto** — low effort, ad ready.
**9. LinkedIn** — post written; Rujal's personal network is warm traffic.

### Tier 3 — Paid (start once measurement is on)

**10. Google Search Ads** — we sell this service; running our own campaign is both
lead-gen *and* a credibility case study. Start after GA4 + conversion tracking are live,
so we can prove cost-per-lead. Budget: start small ($300–500/mo), scale on ROAS.

**11. Retargeting** — the Google Ads tag (AW-17927080637) is already firing site-wide,
so an audience is quietly building. Retarget blog readers with a service ad.

### Tier 4 — Owned / long game

**12. Blog engine** — 2–3 quality posts/week, batch-written and drip-published.
Original content only (see §7).
**13. Newsletter** — subscribe band is live on the homepage; nurture list for repeat touches.
**14. Referrals** — every happy client asked for a review + a referral.

---

## 5. Audience segments

The site tags visitors by content interest so we can build remarketing audiences
once GA4 is connected. Primary target first:

| Segment | Who | Where they enter | What converts them |
|---|---|---|---|
| **Growth-minded businesses** ⭐ *primary* | Owners wanting to automate & scale | AI-automation posts, industry pages | Live AI demo, time-saved framing, free audit |
| Local service businesses | Dentists, trades, salons, clinics, law firms | City + industry landing pages | "Never miss a call", missed-call math |
| E-commerce sellers | Amazon/Walmart sellers | Marketplace pages | Fixed-price packages, "we sell too" |
| Ads-curious | Businesses already spending on ads | Google Ads budget post | ROAS framing, transparent reporting |

**Rule:** every piece of content should name the segment it's for. Blog category ↔
audience segment ↔ retargeting list.

---

## 6. What counts as a lead (and how it's measured)

**Lead = a completed form submission, a click that lands on a booking form, or an
AI voice call started.**

Already firing site-wide via `assets/js/main.js`:

| Event | Trigger |
|---|---|
| `generate_lead` | Any FormSubmit form submitted |
| `form_cta_click` | Any click on a link to `#contact` |
| `ai_call_start` | Visitor starts a call with Nova |

**As of 2026-08-04 these report into GA4 (`G-B064YQYKLC`) as well as Google Ads** —
so source attribution, page-level conversion, and segment performance are all
now measurable. Verified live: both containers registered, events transporting.

**Every link posted anywhere must be UTM-tagged** so we know which platform pays:

```
https://novatoronto.com/?utm_source=kijiji&utm_medium=classified&utm_campaign=web-design
```

`utm_source` = platform · `utm_campaign` = service. Already baked into every
prepared ad.

---

## 7. Content policy (why we don't mass-produce)

The goal is 2–3 quality posts per week, batch-written and drip-published so the
site shows fresh content daily without the risk.

**We do not** auto-rewrite another creator's videos or mass-generate thin posts.
Google's *scaled content abuse* policy targets exactly that, and the penalty is
deindexing — which would bury all 60 pages, not just the new ones. Topics aren't
owned by anyone; we write genuinely original pieces on the same in-demand subjects,
with original diagrams, real sources, and Rujal's byline.

**Post formula that's working:**
lead with the reader's problem → original infographic/diagram → practical steps →
a pull quote → CTA to the free consultation → internal links to the money pages.

---

## 8. Blockers — only Rujal can clear these

| # | Action | Why it matters | Time |
|---|---|---|---|
| 1 | Create **Google Business Profile** | Biggest free local-lead source; currently zero presence | ~15 min |
| 2 | ~~Verify **Google Search Console**~~ ✅ **DONE** — only the sitemap submission is left (type `sitemap.xml` in GSC → Sitemaps → Submit) | Ends SEO blindness | ~1 min |
| 3 | ~~Get **GA4 Measurement ID**~~ ✅ **DONE** — `G-B064YQYKLC` wired site-wide | Reports now live | — |
| 4 | Finish the **Apps Script OAuth** (see `tools/vapi-booking-bridge.gs`) | Bookings land in inbox + calendar automatically | ~2 min |
| 5 | Post the **Kijiji + Facebook ads** | Immediate high-intent traffic | ~30 min |
| 6 | Collect **5 client reviews** | Top local ranking factor | ongoing |
| ~~7~~ | ~~Set an AI Video price~~ ✅ **DONE 2026-08-23** — $497 / $897 / $1,497 published, see §11 | — | — |

---

## 9. 30 / 60 / 90 day plan

**Days 1–30 — Turn the lights on and get listed**
- Clear blockers 1–5 above
- All 4 Kijiji ads posted; refreshed twice weekly
- Facebook Marketplace + 3–5 Toronto business groups
- 5 directory listings (Yelp, YellowPages, 411, Bark, Alignable)
- 8–10 new blog posts (2–3/wk), drip-published
- Ask every past client for a review
- **Success = first inbound lead from a tracked source, and GSC showing pages indexed**

**Days 31–60 — Prove a channel, then feed it**
- Read GSC: which queries are we impressing on but not ranking for? Write/expand for those
- Double down on whichever channel produced leads; drop what didn't
- Launch a small Google Search campaign on our best-converting service
- Add 3–5 more city or industry pages targeting proven query patterns
- Build first remarketing audience in GA4
- **Success = a repeatable cost-per-lead number**

**Days 61–90 — Scale what pays**
- Increase ad budget only where ROAS justifies it
- Turn best-performing blog posts into a lead magnet for the newsletter
- Case study from the first client win — the strongest sales asset there is
- Consider putting Nova on the real phone line (365-355-3133)
- **Success = predictable monthly leads and a case study to sell with**

---

## 11. AI Video pricing — what the market research found (2026-08-23)

Six independent research sweeps, each fact-checked by an adversarial verifier
that refetched every source URL. 161 datapoints collected, **138 kept** (8
Fiverr rows discarded as unverifiable behind a bot wall, 14 vendors publish no
number, 1 stale). 40 of 48 re-checked prices confirmed live.

| Segment | Low | Median | Average | High | n |
|---|---|---|---|---|---|
| **AI brand video, done-for-you agency** (CAD @ 1.38) | $690 | $2,759 | **$3,220** | $6,900 | 6 |
| **Toronto/GTA traditional filmed promo, entry tier** | $1,500 | $3,000 | $3,043* | $10,000 | 14 |
| Freelance marketplaces (PeoplePerHour, single video) | — | $62 | $99 | $407 | 10 |
| Self-serve AI platforms (DIY) | $40/mo | — | — | $345/mo | 8 |

\* excluding one $10,000 outlier; mean and median converge on ~$3,000.

**Rujal asked to "use the average price." The average is $3,220 — and we did
not use it.** At $3,220 a 30-second video would cost more than the entire
E-commerce website package ($2,000) and 64% of Gold ($5,000). It would make
every other price on the site look arbitrary. It is also a thin, top-heavy
sample: drop Lemonlight's $5,000 and the average falls 23% to $2,483. Our
buyer (GTA clinics, trades, salons) spends $500–1,500/mo on *ad spend* total.
**This is reversible in one pass if Rujal wants the literal average.**

### What we published instead

$497 / **$897** / $1,497 (+HST). Silver is the intended sale and is exactly the
Do Home Healthcare video. 3.0x bottom-to-top; Toronto video ladders run
2.7x–4.3x, so we sit dead centre. $897 is 70% below the Toronto filmed median,
72% below the AI-agency average, and 14x the freelance median — cheap enough
to be an easy yes, expensive enough to signal real work. It sits just under
Bronze website ($900) so the whole page reads as one ladder.

**Deliberately no "Custom — contact us" tier.** Per Awesomic's own roundup, 10
of 11 AI-video agencies publish no rate card at all, and no Canadian agency
publishes one in CAD. Publishing real numbers *is* the positioning.

### Two confirmed gaps in this market

1. **No Canadian agency publishes a CAD rate card for AI video.** Not one.
2. **No Canadian agency publishes a website + video bundle price.** Not one.
   (Azuro Digital, a Toronto web shop, says outright that video "isn't
   something we do.") Hence the **$1,400 Launch Bundle** — website + brand
   video, live in ~2 weeks. Lead with this; nobody in the GTA has published it.

Third gap: **speed**. Signature Video Group publishes 4 weeks on its $3,500
package, 6 weeks at $15,000. Nobody in Toronto advertises days.

### Risks to watch

- **DIY collapse.** Creatify is CA$54/mo for ~20 videos, and that price is
  confirmed live. *Never sell "AI video" — sell the script, the brand
  direction, the revisions, and a finished asset that matches their site.
  Price the judgment, not the render.*
- **Freelance undercut.** PeoplePerHour median CA$62. *Compete on local,
  named, accountable, invoiced in CAD — never on price.*
- **One case study.** Take 3 more videos at Bronze pricing inside 60 days,
  even at cost. Portfolio is what unlocks the next price band. Revisit Silver
  once 5 videos are live.
- **Cap revisions in writing.** 2 rounds is the published industry standard.
  Unlimited revisions on an $897 product eats the margin fastest.
- **AI disclosure in regulated verticals.** Healthcare/legal/financial clients
  may have trust or compliance concerns with synthetic people. A
  footage-plus-motion-graphics variant is offered on the page as the safe
  option.
- **Always publish "+HST"** or $897 invoices at $1,013.61 and reads as
  bait-and-switch.
- **Re-check these six URLs every 6 months** — this category re-prices fast:
  gisteo.com · mawaistudios.com · marmalaide.ai · creatify.ai · lemonlight.com
  · lapseproductions.com

---

## 10. Do-not-do list

- Don't buy backlinks or use "SEO packages" from cold emailers — penalty risk
- Don't mass-publish AI content (see §7)
- Don't pay to promote a classified until the free version has run 2 weeks
- Don't add more services beyond AI Video (added 2026-08-23) — sharpen the five we have
- Don't rebuild the website again — it converts fine; the gap is traffic
