---
name: design-audit
description: Audit a website's UI/UX and produce a prioritised, evidence-backed report - visual hierarchy, typography, spacing, colour contrast, CTA/conversion clarity, mobile responsiveness at 375px, design-system consistency, accessibility, and perceived performance. Every finding carries a measured number, a file:line, and a concrete fix. Use this whenever the user asks for a design review, design audit, UX audit, accessibility check, contrast check, "does this look right", "how does my site look", "review the design", "is my site converting", "check it on mobile", or asks why a page feels off, cluttered, or unprofessional - even if they don't say the word "audit". Also use it before and after any significant redesign of a page or section, and when adding a new section to an existing site to check it matches the established design system.
---

# Design Audit

You are auditing a real site that a real business depends on. The point is not to
produce a tasteful list of opinions — it is to find the specific things costing
the owner money or credibility, prove them with numbers, and say exactly how to
fix each one.

## What separates a useful audit from a useless one

A useless audit says "improve visual hierarchy" and "consider more whitespace."
Nobody can act on that.

A useful audit says: *"The hero CTA is `#0096DD` on `#F7FBFD` — contrast 3.1:1,
below the 4.5:1 minimum. On a phone in daylight it disappears. `index.html:412`.
Darken to `hsl(199,100%,34%)` for 4.6:1."*

The difference is **a measured value, a location, and a fix.** Hold every finding
to that bar. If you cannot measure it or locate it, either go measure it or drop it.

## Workflow

### 1. Establish what the site is for

Before measuring anything, know what a conversion is. A lead-gen agency site lives
or dies on form submissions and phone calls; an e-commerce site on add-to-cart; a
content site on time-on-page and subscribes. Read the page, and any project
`CLAUDE.md`, to find the actual goal. Findings get ranked by impact on **that**
goal, not by how offensive they look to a designer.

Ask the user which URL or local path to audit if it is not obvious. Prefer the
live site when one exists — that is what customers actually see.

### 2. Open it and force a real viewport

Use the Browser pane. Then, before measuring anything:

```
resize_window with explicit width and height (e.g. 1280 x 900)
```

**This step is not optional and skipping it will silently corrupt every number you
collect.** When the preview pane is not compositing — which is common — the tab
reports `window.innerWidth === 0`. Grid columns compute to `0px`, cards measure
18px wide, and you will "discover" a horizontal overflow bug that does not exist.
Screenshots come back blank or stale for the same reason.

So: **measure with `javascript_tool`, not with your eyes.** Screenshots are a
nice-to-have for the report, never the evidence. Every probe result below starts
by reporting the viewport — if it reads 0, stop and call `resize_window` again.

### 3. Run the probe

`scripts/probe.js` collects the whole measurement set in one pass. Read the file,
paste its contents into `javascript_tool`, and it returns structured JSON covering
typography, spacing, contrast, tap targets, overflow, heading order, alt text,
focus states, token usage, and performance.

Run it twice — once at **1280×900** and once at **375×812** — because most real
problems are mobile-only. Reload between the two so layout-dependent measurements
(LCP, overflow) are honest.

`references/thresholds.md` has the pass/fail lines for every metric and what each
one actually means for a visitor. Read it when interpreting results.

### 4. Trace each finding back to source

A measured number is only half a finding. Grep the repo for the offending selector
or value so you can name the file and line. A report the owner can act on without
hunting is worth several times one they have to investigate.

### 5. Judge the things numbers cannot catch

The probe cannot tell you whether the page makes sense. Read the actual copy and ask:

- **Scan path** — following only headings, buttons and images, does the page tell a
  coherent story? Where does the eye go first, and is that the most valuable thing?
- **The five-second question** — from the top of the page alone, can a stranger say
  what is sold, to whom, and what to do next?
- **CTA competition** — count the competing calls to action above the fold. More
  than two and each one gets weaker.
- **Proof placement** — do claims sit next to evidence, or are testimonials and case
  studies stranded at the bottom where nobody reaches?
- **Section rhythm** — does every section look the same weight? A page where
  everything shouts reads as a page where nothing matters.

### 6. Write the report

Rank strictly by **impact on the conversion goal**, not by severity of the CSS crime.
A 3.9:1 contrast ratio on a footer link matters far less than a form that is hard to
find. Use this structure:

```markdown
# Design Audit — [site] — [date]

**Audited:** [URLs] at 1280x900 and 375x812
**Conversion goal:** [what counts as a win]

## Verdict
[2-4 sentences. What is actually wrong, and what is the single highest-value fix.]

## Critical — costing conversions now
### 1. [Finding]
- **Measured:** [the number]
- **Where:** `file.html:123`
- **Why it costs you:** [tie to the goal, concretely]
- **Fix:** [specific change, with the value to use]

## Important — credibility and polish
[same structure]

## Minor — worth doing eventually
[same structure, can be terser]

## What is already working
[Genuine strengths. Do not pad this - but do not skip it either: the owner needs
to know what NOT to break in the next redesign.]
```

Then offer to implement the fixes. Do not implement them as part of the audit
unless asked — the owner should get to choose.

## Judgement notes

**Do not redesign the site in the report.** The owner has usually made deliberate
choices. If the palette is on-brand and the layout works, say so and move on. An
audit that concludes "rebuild it" is almost always wrong and always unwelcome.

**Separate objective failures from taste.** A 2.8:1 contrast ratio is a fact. "The
hero feels dated" is an opinion — you may still say it, but label it as taste and
put it in Minor.

**Weight new sections harder.** Recently added sections are where design systems
drift: hardcoded hex values instead of tokens, one-off spacing, a fourth font size.
The probe's `tokens` section surfaces this. Drift is cheap to fix now and expensive
later.

**Say when something is fine.** If contrast passes everywhere and tap targets are
all comfortable, report that plainly. Inventing findings to look thorough destroys
the value of the ones that are real.
