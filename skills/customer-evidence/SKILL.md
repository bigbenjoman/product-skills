---
name: customer-evidence
description: "Mine customer feedback into a ranked, segmented list of problems with verbatims — app-store and review-site reviews, NPS comments, leaving/cancellation surveys, support tickets, sales-call notes, forum threads and interview transcripts. Use when the user wants to know what customers complain about, what the biggest pain points are, voice of the customer, review mining, churn reasons, or needs evidence for the problem paragraph of a PR/FAQ or items for a MaxDiff study. Also builds a competitor feature benchmark matrix."
metadata:
  version: 0.2.0
---

# Customer Evidence

Working Backwards begins with the customer's problem. Most teams assert it. This skill **evidences** it, with counts and verbatims, so that the PR/FAQ problem paragraph and the MaxDiff item list rest on what customers actually said.

## Step 1: Collect

Ask which sources exist. Prefer behaviour and unprompted complaints over opinions:

| Source | Strength | Watch out for |
|---|---|---|
| App store / review sites (yours and competitors') | Unprompted, public, competitor-comparable | Skews to extremes |
| Leaving / cancellation survey | Closest to churn | Usually tick-boxes; read the free text |
| Support tickets / chat logs | Volume and severity | Dominated by bugs; strip PII first |
| NPS verbatims | Segmentable by score | Promoter comments are rarely actionable |
| Sales-call / lost-deal notes | B2B buying criteria | Salesperson's paraphrase, not the customer's |
| Interviews | Depth, the "why" | Small n; don't count them as votes |

Never paste personal data into outputs. Redact names, emails and order numbers.

**Lawful basis (UK/EU GDPR):** analysing your own support tickets and survey answers to improve the product is usually *legitimate interests*. Record a short legitimate-interests assessment, minimise what you keep, and delete raw exports after coding. Public reviews: respect each site's terms of use. Don't scrape where it's prohibited; export or sample by hand instead.

**Interviews:** a different instrument from mining. Read `references/interviews.md`. Never count interview mentions as votes.

**Minimum samples for mining:**
- **Codebook:** 50–100 items to build it.
- **Ranking themes:** 300+ items for stable frequencies.
- **Segment comparison:** 100+ items per segment.

Weight the last 90 days more heavily than older items. Discard obvious spam or bot reviews (duplicate text, review bursts, no purchase context).

## Step 2: Code

1. Read a sample of 50–100 items and draft a **codebook**: 10–25 problem themes, each with a one-line definition, an inclusion rule and an example. See `references/codebook-example.md`.
2. Code every item, allowing multiple themes per item. Record segment fields (platform, plan, country, tenure, NPS band).
3. Spot-check 10% by hand. If more than about 1 in 10 are coded differently, refine the codebook and re-run.

## Step 3: Rank

For each theme:
- **Frequency:** % of items mentioning it
- **Severity:** 1–3, using the anchors in `references/severity-rubric.md`. 3 = stops the job; 2 = workaround needed; 1 = irritation.
- **Trend:** this period vs last
- **Segment skew:** where it over-indexes

Rank by frequency × severity. Keep **3 verbatims per theme**, the most vivid and specific. These go straight into the PR/FAQ problem paragraph.

## Step 4: Benchmark competitors (optional)

Build a matrix: rows are customer-facing capabilities drawn from the themes; columns are you, 3–8 named competitors **and the status quo** (what people do today without any product).

Mark ✓ / ✗ / partial. Add a priority column, P1–P4. P1 means a gap that customers name and every competitor fills.

## Output

1. A one-page summary: the top 5 problems, with frequency, severity and 2 verbatims each
2. The full theme table
3. The competitor matrix
4. A **MaxDiff item list**: themes rewritten as solution items in customer language, ready for the `maxdiff-study` skill
5. A draft **problem paragraph** for the `working-backwards` skill

## Mistakes

- Counting interview mentions as if they were survey votes
- Treating support volume as demand. Bugs dominate ticket volume.
- Writing themes as solutions ("needs AI search") instead of problems ("can't find last night's match")
