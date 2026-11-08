---
name: market-analysis
description: "Outside-in market and competitor analysis to feed a product strategy: translate the company mission and commercial strategy into product goals, size and choose markets (outside-in indicators such as GDP coverage, digital readiness, category penetration — deepen before you expand), build a competitor feature benchmark with customer-vote % and P1–P4 priority, and use third-party data (device installed base, payment-method share, app-store spend) to decide platform and payment coverage. Use when the user asks for competitor benchmarking, market sizing, which markets to enter, which devices or platforms to support, which payment methods, ideation workshop prep, or the 'Gather' stage of product strategy."
metadata:
  version: 0.2.0
---

# Market Analysis (the Gather stage)

This skill covers the outside-in half of the Gather stage. The inside-out half, listening to customers, is `customer-evidence`. Behavioural data is `metrics-and-wbr`.

## 1. From mission to product goals
Ask for, or read:
- the mission
- the commercial strategy and targets (revenue, EBITDA, subscribers, by market)
- the existing product strategy

Write a **one-page translation**: each commercial goal becomes the product outcome that would move it. Example: "grow subscribers in the US" → "raise US review density before entering new markets".

Each product goal needs a metric. Any goal without one is an aspiration; label it as such.

## 2. Outside-in market selection: a weighted scorecard
Use `references/market-scorecard.md`.
1. **Pick 4–6 indicators that fit YOUR product.**
   - Consumer: addressable population or GDP covered, digital readiness, category penetration, usage depth (e.g. reviews per website), payment readiness, regulatory barriers.
   - B2B or micro: number of target businesses, their tool spend, language, partner reach.
2. **Normalise each to 0–100:** (value − min) ÷ (max − min) × 100. Invert any where lower is better.
3. **Weight them**, summing to 100%, and write down why.
4. **Score = Σ weight × normalised value.** Rank, then sanity-check the top 3 by hand.

Rule of thumb from practice: **deepen before you expand.** Where you already have coverage but low usage depth is usually cheaper to win than a new country.

## 3. Competitor benchmark (two views, one method)
**View A: customer decision criteria** (for strategy and the PR/FAQ):
- Rows are the 5–8 criteria customers actually use to choose (from interviews and reviews).
- Columns are you, 3–6 named competitors, **and the status quo** (what they do today with no product).
- Score each cell 1–5 with a one-line source.
- **You must lose at least one row to a named competitor.** If you win every row, you picked rows you win.

**View B: feature parity** (for the backlog):
1. List 15–25 customer-facing features and fill in ✓ / ✗ per competitor, citing source and date.
2. Add **customer vote %**, measured properly. Use a forced-choice method: MaxDiff share or a "pick your top 5" ranking (`maxdiff-study`). A 1–5 rating question makes everything look important.
3. Assign P1–P4:

| Priority | Rule |
|---|---|
| P1 | High vote AND most competitors have it (a parity gap customers notice; the launch slips without it) |
| P2 | High vote, few competitors have it (a chance to differentiate) |
| P3 | Medium vote |
| P4 | Low vote, or cost far above value |

4. **Write down every override**, e.g. "70% vote but P3: needs a rights deal we don't have".

## 4. Third-party data for coverage decisions
Answer "which devices, platforms and payment methods, and in what order?" with data:
- your share of minutes or sessions by platform, set against the installed base
- app-store share of customer spend (e.g. one platform taking about 65% of spend justified building for it first)
- payment-method share by market

Output: a ranked coverage roadmap with the % of the audience reached at each step.

## 5. Ideation workshop pack
Use the run sheet in `references/workshop-run-sheet.md`: 2 hours, 6–10 people across product, UX, engineering, marketing and the business. The output is a long list ready for RICE+.

## Outputs
1. Mission → product goals page
2. Market scorecard
3. Benchmark matrix with customer vote and P1–P4
4. Coverage roadmap
5. Workshop pack
