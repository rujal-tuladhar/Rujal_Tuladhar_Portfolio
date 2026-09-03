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
cd C:\Users\Rujal\Documents\GitHub\Rujal_Tuladhar_Portfolio
python tools/blog/publish_post.py tools/blog/posts/<file>.json --date <YYYY-MM-DD>
```

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
