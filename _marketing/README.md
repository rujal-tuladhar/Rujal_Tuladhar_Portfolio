# Nova Toronto — Marketing Folder

Everything marketing for novatoronto.com lives here. This folder is **not**
published to the live site (underscore folders are excluded from the build),
so the playbook stays private.

## Start here

| File | What it is |
|---|---|
| **[MARKETING-PLAN.md](MARKETING-PLAN.md)** | ⭐ **The strategy.** Situation, positioning, channel priority, audience segments, lead measurement, content policy, blockers, and the 30/60/90-day plan. Read this first. |
| [kijiji-ads.md](kijiji-ads.md) | 4 ready-to-paste Kijiji ads (one per service) with categories, titles, prices |
| [classifieds-facebook-craigslist.md](classifieds-facebook-craigslist.md) | Facebook Marketplace + business-group posts, and a Craigslist Toronto ad |
| [directories-and-outreach.md](directories-and-outreach.md) | Google Business Profile copy, Yelp/YellowPages/411 blurbs, Clutch/Bark profiles, LinkedIn post, cold-DM and reply templates |

## The one rule: tag every link

Every link you paste anywhere must carry UTM tags so we can tell which
platform actually produces leads:

```
https://novatoronto.com/?utm_source=kijiji&utm_medium=classified&utm_campaign=web-design
```

`utm_source` = platform · `utm_campaign` = service
(`web-design` | `marketing` | `ai` | `marketplace-selling`)

Every prepared ad in this folder already has this baked in.

## Next actions (highest return first)

1. **Google Business Profile** — copy is in `directories-and-outreach.md`
2. **Google Search Console** — verify + submit `sitemap.xml`
3. **GA4 Measurement ID** — send the `G-XXXXXXX` to Claude to wire up reporting
4. **Post the Kijiji ads** — all 4, refresh every 3–4 days
5. **Facebook Marketplace + Toronto business groups**

Full reasoning and the 30/60/90-day plan: [MARKETING-PLAN.md](MARKETING-PLAN.md)

## Posting log (fill in as you go)

| Date | Platform | Ad / profile | Live link | Renewed |
|---|---|---|---|---|
|  |  |  |  |  |

## Rules of thumb

- **Answer fast.** Classifieds buyers hire whoever replies first — reply template is in `directories-and-outreach.md`.
- **Photos matter.** Use portfolio screenshots from `assets/img/`; ads with 3+ images get far more clicks.
- **Lead with the AI demo.** "Talk to our AI right now on our website" is the strongest hook we have — no GTA competitor offers it.
- **One ad per Kijiji category**, varied text — don't duplicate.
- **Don't pay to promote** until a free listing has run 2 weeks and produced enquiries.
