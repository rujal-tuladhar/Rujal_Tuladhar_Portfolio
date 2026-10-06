# Daily AI blog — runbook

One original post per day on AI and tech for small-business owners, published to
novatoronto.com with verified outbound links, dated, bylined "Rujal Tuladhar",
and surfaced on the homepage. This file is the authoritative recipe; the
scheduled task's SKILL.md just points here.

## The rule that matters most

**A post is only worth publishing if every fact in it came from a page you
actually fetched today.** Never invent a product, price, feature, date or
statistic. If a fact cannot be verified, leave it out — a shorter true post
beats a longer one with a made-up price in it. Google's scaled-content-abuse
policy deindexes sites that mass-publish thin or copied content; that would
bury all 60+ pages on this site, not just the blog. Original, sourced, useful
— every day — is the whole game.

## Files

| Path | What |
|---|---|
| `tools/blog/publish_post.py` | Validates + renders + updates homepage/index/sitemap + commits + pushes |
| `tools/blog/post_template.html` | The post page template |
| `tools/blog/published.json` | Log of every published post — read it FIRST to avoid repeating a topic |
| `tools/blog/posts/<date>-<slug>.json` | The JSON spec for each post (keep them; they are the audit trail) |
| `assets/img/blog/<slug>.jpg` | Generated 1200×630 cover, made by the publisher |

## Daily run (≈ 20–30 min of agent time)

### 1. Pick the topic — don't repeat yourself

Read `tools/blog/published.json`. Do not publish a topic that appears in the
last 30 days. Rotate through these angles so the blog stays varied:

- **Tool roundups** — "best AI X for 2026" (video generators, voice agents,
  image tools, writing tools, receptionists, ad creative tools, website
  builders). These rank well and link naturally to Nova's services.
- **Weekly AI news for business** — the 3–5 developments in the last 7 days
  that change what a small business can do or what it costs.
- **How-to / decision guides** — "should a dentist use an AI receptionist",
  "how much does Google Ads cost in Toronto in 2026", "AI video vs filmed video".
- **Local angle** — Toronto/GTA-specific: costs, regulations (e.g. CASL, AI
  disclosure), local case studies.

Pick something a GTA small-business owner would actually search for. Check
the news first: if something big happened in AI this week, that beats a
scheduled roundup.

### 2. Research — with WebSearch + WebFetch, nothing from memory

Run at least 5 distinct searches. For every claim you plan to use, **fetch the
actual page** and keep: the URL, the site name, a short quote, and the date on
the page. Prefer official product/pricing pages and sources dated 2026. Flag
anything older than 2025 and prefer not to use it.

Then verify adversarially: re-open each source and confirm it really says
what you noted. Drop anything you cannot personally see on the page today.

Aim for 8–15 verified facts before writing. Fewer than 6 → pick a different
topic; you don't have enough to write something true.

### 3. Write the post JSON

Save to `tools/blog/posts/<YYYY-MM-DD>-<slug>.json`. Exact shape:

```json
{
  "slug": "best-ai-video-generators-2026",
  "title": "Under 70 chars, specific, no clickbait",
  "category": "AI Tools | AI News | AI Automation | Digital Marketing | Website Design",
  "excerpt": "Under 160 chars. Used as the meta description and card text.",
  "keywords": "6-10 comma-separated terms",
  "cover_title": "Under 40 chars, for the cover image",
  "intro_html": "<p>One or two paragraphs. Open with the reader's problem.</p>",
  "glance": [ { "icon": "uil-video", "heading": "...", "sub": "..." } ],
  "sections": [
    { "heading": "...", "body_html": "<p>...</p>", "takeaway": "one sentence: what this means for a GTA small business" }
  ],
  "bottom_line_html": "<p>...</p>",
  "sources": [ { "label": "Site — Article title", "url": "https://..." } ],
  "related": [ { "label": "...", "href": "../../index.html#ai-video" } ]
}
```

Constraints the publisher enforces (it will refuse to publish otherwise):

- 800–1,800 words of body text; 3–6 glance items; 4–7 sections
- at least 4 sources on at least 3 different domains, none of them novatoronto.com
- **every outbound URL must be reachable** (checked live with curl)
- body HTML may only use `<p> <a> <strong> <em> <ul> <ol> <li> <br>`
- internal links are relative to the post folder: `../../index.html#ai-video`,
  `../../ai-automation/`, `../../digital-marketing/`, `../<other-post-slug>/`
- glance icons are Unicons classes (`uil-video`, `uil-dollar-alt`, `uil-bolt`,
  `uil-robot`, `uil-chart-line`, `uil-clock`, `uil-shield-check`, …)

House style (this format has performed well):

- Open with the reader's problem in the first sentence
- Plain English, short paragraphs, no hype words ("revolutionary",
  "game-changing", "in today's fast-paced world")
- Every section ends with a concrete "what it means for you"
- Name tools, versions, prices, limits — vague advice is worthless
- **Link out generously** to official pages and independent reviews using
  `<a href="…" target="_blank" rel="noopener">`. Outbound links are a feature.
- One honest recommendation per use-case, and say who should NOT bother
- End with a natural bridge to a Nova Toronto service — not a hard sell
- Synthesise across sources in your own words; never mirror one source's structure

### 4. Publish

```
python C:/Users/Rujal/Documents/GitHub/Rujal_Tuladhar_Portfolio/tools/blog/publish_post.py C:/Users/Rujal/Documents/GitHub/Rujal_Tuladhar_Portfolio/tools/blog/posts/<file>.json --date <YYYY-MM-DD>
```

Use the absolute paths exactly as shown and do not `cd` first - the scheduled run is
only pre-approved for this exact command shape, and the publisher locates the repo from
its own path.

It validates first and aborts before writing anything if a check fails —
read the message, fix the JSON, re-run. On success it generates the cover,
writes the post, adds the blog-index card, the homepage slider slide and the
homepage "latest post" strip, updates `sitemap.xml` and the generator's
`STATIC_URLS`, appends to `published.json`, commits and pushes. Credentials
are cached in Git Credential Manager; no prompt appears.

Use `--dry-run` to validate without writing, `--no-push` to write without
committing (useful when checking the render locally).

### 5. Confirm it is live

Wait ~2 minutes for GitHub Pages, then:

```
curl -s -o /dev/null -w "%{http_code}" https://novatoronto.com/blog/<slug>/
```

Expect `200`. Then finish with a two-line report: the title, the URL, the word
count, and the number of sources.

## Lead posts: the 100-topic calendar and the ready queue (added 2026-10-02)

Rujal asked for a post every day that promotes a Nova service and brings leads. These are
EVERGREEN buyer-intent posts (cost, comparison, how-to, industry problem, Canadian rules),
separate from the weekly AI news post.

| Path | What |
|---|---|
| `tools/blog/_queue/calendar.json` | The 100 topics in publishing order: n, slug, title, primary_keyword, service, outline |
| `tools/blog/_queue/NNN-<slug>.json` | A fully written, validated post waiting to go out (NNN = calendar n, zero-padded) |
| `tools/blog/_queue/state.json` | Last queue publish date (one queued post per day, enforced by the publisher) |
| `tools/blog/_queue/failed/` | Posts that failed validation at publish time (usually a source went dead) |

The folder starts with an underscore so GitHub Pages does not serve drafts.

### Every day, in this order

1. **Publish the next ready post (cheap, do this FIRST):**
   ```
   python C:/Users/Rujal/Documents/GitHub/Rujal_Tuladhar_Portfolio/tools/blog/publish_post.py --next
   ```
   It picks the lowest-numbered file in `_queue/`, validates it (live link check), publishes with
   today's date, moves the JSON to `posts/<date>-<slug>.json`, commits and pushes. If a post fails
   validation it is moved to `_queue/failed/` and the next one is tried. It refuses to publish a
   second queued post on the same day. Then confirm the URL returns 200 as in step 5 above.

2. **Top up the queue by ONE post** if it holds fewer than 10 ready posts: take the lowest `n` in
   `calendar.json` whose slug is neither in `published.json` nor already a file in `_queue/`.
   Research and write it exactly as steps 2-3 above (every fact fetched today, 900-1,400 words),
   keep the calendar slug, add a `faq` array (3-5 real buyer questions, plain-text answers under
   600 chars), end with a bridge to the calendar item's service page, save it as
   `tools/blog/_queue/NNN-<slug>.json`, and validate with:
   ```
   python C:/Users/Rujal/Documents/GitHub/Rujal_Tuladhar_Portfolio/tools/blog/publish_post.py C:/Users/Rujal/Documents/GitHub/Rujal_Tuladhar_Portfolio/tools/blog/_queue/NNN-<slug>.json --dry-run
   ```
   Fix until it passes. If usage is short, skip the top-up - publishing comes first.

3. **AI news post: Mondays only** ("AI This Week", the original daily recipe above), or any day
   something big happens. On other days the queued lead post IS the day's post.

4. If something is in `_queue/failed/`, repair it when there is time: replace the dead source or
   drop that fact, move the file back into `_queue/`, dry-run again.

### Extra fields the publisher now understands

- `"faq": [ { "q": "Question ending in ?", "a": "Plain-text answer, no HTML, under 600 chars" } ]`
  (optional, 3-6 items). Rendered as a "Common questions" section and as FAQPage structured data.
- Covers are drawn by `tools/blog/cover.py`: an original illustration picked from the slug
  (website, chart, shop, phone, video, automation, news, rules, course). No stock photos.
  `python tools/blog/cover.py` renders a sample of each style into `_cover_samples/`.
- Every lead post should link once to the free course: `../../ai-course/` ("free AI course for beginners").

## If something is wrong

- **Push fails** → do not retry blindly. Report the error. Rujal may need to
  re-authenticate Git Credential Manager.
- **A source 404s during validation** → find a replacement source for that
  fact or remove the fact. Never publish with a dead link.
- **Fewer than 6 verified facts** → change topic. Do not pad.
- **Slug already exists** → you are repeating a topic; check `published.json`.

## Run notes

_(append dated notes here when something about the process changes)_

- **2026-09-02** — First real post (30 sources) hit three curl `000` results:
  adobe.com x2 and globenewswire.com. All were live pages behind bot walls
  (curl exit 92 in 0.16s = HTTP/2 refused to a non-browser client; Python got
  TLS/timeouts). The validator now DNS-resolves any `000` host: resolvable =
  bot wall, allowed and shown as `wall`; unresolvable = dead, still refused.
  Real 404/410s are unaffected. So: a `wall` line is fine **only if you fetched
  that page in the browser during research** - that is what the recipe already
  requires. Never add a source you did not open.

- **2026-09-03** — Corrections: to change a post that is already live, edit its JSON in
  `tools/blog/posts/` and re-run the publisher with `--update` and the ORIGINAL
  `--date`. It re-renders the page and cover in place, swaps the slider slide and
  blog-index card, updates the homepage strip only if that post is still the newest,
  bumps the sitemap `lastmod`, and keeps the original publish date in the log. The
  daily run never uses `--update`, so the unique-slug guard still protects it.
  First used to re-rank the AI-video roundup to Rujal’s order: Seedance 2.5 > Kling 3.0 > Veo 3.1.

### 2026-09-19 - homepage got duplicated by the Sept 18 run (fixed)
- Cause: index.html had mixed line endings after a hand edit with `sed -i`. The publisher looked for CRLF to find the end of the marker line, found the first one ~2,300 lines lower, and re-pasted the page body. Every section and every post showed twice.
- Fix: homepage rebuilt from the last good commit plus the Sept 18 slide and strip. `publish_post.py` now uses `eol_after()` (bare LF), `nl_of()` is a majority vote, and `guard_homepage()` aborts if any landmark is not exactly once or the file changes by more than 8,000 chars.
- Rule: never hand-edit index.html with `sed -i` on Windows. Use a Python read/write with `newline=""`, and check `git diff --stat` shows only the lines you meant to touch.

### 2026-10-06 - calendar is now 300 topics; photo covers
- `tools/blog/_queue/calendar.json` holds 300 topics (n 1-300). Every topic has an `image_prompt`. The top-up rule is unchanged: write the lowest n that is neither published nor queued.
- Photo covers: if `tools/blog/_photos/<slug>.jpg` exists (a "/" in the slug becomes "--"), the publisher uses it as the post cover automatically. If it does not exist, the drawn cover from `cover.py` is used. Nothing to do at publish time.
- The photos are generated BY RUJAL, by hand, on higgsfield.ai (Nano Banana Pro, 16:9, 2K, Unlimited on) from `Desktop
ova-social\image-prompts.html`, then filed with `python Desktop
ova-social\images\image_tools.py collect`. Never automate the Higgsfield website: its Unlimited plan is for human use only, and generating through the CLI or connector spends credits. Do not generate images in the scheduled run.
- `python tools/blog/apply_photos.py` gives already-published posts their photo cover (older hand-built posts get their hero and social image repointed).
