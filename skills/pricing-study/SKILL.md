---
name: pricing-study
description: "Run consultancy-grade pricing and packaging research for a new or existing product at startup cost: option space, competitor price/packaging benchmark, willingness-to-pay survey (Van Westendorp with NMS extension, Gabor-Granger or monadic price cells), pricing-power scorecard, interest x WTP matrix, Good-Better-Best tier design with fences, billing/annual-discount/price-increase and grandfathering tests, revenue modelling and a decision report. Use when the user asks what to charge, pricing strategy, willingness to pay, Van Westendorp, Gabor-Granger, price sensitivity, tiers, packaging, freemium, price increase, or monetisation."
metadata:
  version: 0.1.0
---

# Pricing Study

A top-tier consultancy pricing programme follows a recognisable shape. Each phase narrows what the next one tests:

1. Agree objectives
2. Agree the option space with Product
3. Benchmark competitors
4. Survey willingness to pay
5. Segment
6. Design packages
7. Model the money
8. Recommend

About 70–80% of the analytic labour in that shape can now be done by an agent plus an online panel. One example: a two-phase study on an online panel, for two to three thousand pounds in all, can move a launch price a long way. In a SYNTHETIC example, Fernhill Coffee: the founders assumed £8; the study pointed to £14.

**Be honest about the limits.** Read `references/when-you-need-an-expert.md` before telling the user they don't need a consultancy.

## Step 0: The decision and the option space

Ask the user, and write the answers down:

- **The decision.** Launch price? Tier structure? A price rise? Freemium or trial?
- **The value metric:** what the customer pays *per*. Per seat, per subject, per usage, per location.
- **The option space.** Every variable a package could differ on, each tagged with one of: feasible now / decision pending / later / out. Only test what you could ship.
- **Constraints:** costs (floor price), contracts, channel or app-store fees, regulation.

## Step 1: Competitor benchmark (desk research — fully automatable)

Read `references/benchmark-framework.md`.

- Cover 10–30 competitors: direct ones plus adjacent ones the customer also pays for.
- Compare them on four ways to differentiate a package: **Content/Scope, Functionality, Advertising, Access** (seats, devices, usage limits).
- Also compare: number of tiers; price ladder and the % step between tiers; add-ons; annual discount; trial vs freemium.
- **Log the source URL and capture date for every price.** Prices vary by geography and change.

## Step 2: Willingness-to-pay survey

Read `references/survey-modules.md` and choose modules:

| Module | Answers | Notes |
|---|---|---|
| **Van Westendorp** (4 questions) + NMS purchase-likelihood | Acceptable price range, optimal price point | Best first study. The NMS extension gives a demand and revenue curve |
| **Gabor-Granger** (adaptive ladder) | Demand and revenue at specific prices | Analyse from each respondent's **maximum accepted price**: demand(p) = share of ALL respondents whose max ≥ p. The curve is monotonic by construction; if yours isn't, the analysis is wrong (you divided by the people *shown* each price) |
| **Monadic price cells** (each respondent sees one price, e.g. −50/−20/0/+20/+50%) | Cleaner price response and elasticity | Needs about 100+ per cell. Use it for price rises on an existing product |
| **Interest × WTP matrix** per feature/content item | Hero / Niche / Nice-to-have / Lower-value | A cheap way to get item-level WTP. Pair it with the `maxdiff-study` skill |
| **Pricing-power scorecard** (existing customers) | Whether you can raise prices | Combines value-for-money, NPS, price recall and % "expensive" |
| **Billing & evolution** | Monthly vs annual, discount threshold, increase tolerance, grandfathering | Find the cliff before you hit it |
| **Choice-based conjoint** | Package design trade-offs, share simulation | Expert territory. See `when-you-need-an-expert.md` |

**Rules**
- Use the **same stimulus** for everyone, and put the marketing claims you will actually use into it. In one study, a credential that was not in the stimulus later moved interest for 58.8% of respondents, so the stimulus understated demand.
- Run phases in sequence. Phase 1 (Van Westendorp) sets the range; Phase 2 (Gabor-Granger or monadic) tests points inside it. Exclude Phase 1 respondents from Phase 2.
- Field on Prolific or a similar panel. Cost formula and sample rules are the same as in `maxdiff-study/references/fielding.md`. Check current fees on the vendor's site; never quote them from memory.

## Step 3: Analyse

Run `scripts/pricing_toolkit.py`:

- `van_westendorp(...)` returns PMC, OPP, IDP and PME (point of marginal cheapness, optimal price point, indifference price point, point of marginal expensiveness).
- `gabor_granger(prices, max_wtp)` returns cumulative demand and a revenue index. `gg_from_segments()` does the same from a "share whose max price is X" table.
- `nms_curves()` turns the NMS likelihood answers into demand and revenue curves. The calibration weights (top box 0.7, second box 0.3) are an assumption, so write that down.
- `net_revenue()`, `ltv()`, `payback_months()` and `arc_elasticity()` give the economics.

Then:

1. **Validate Van Westendorp answers.** Drop anyone whose answers aren't ordered too cheap < cheap < expensive < too expensive, and report how many you dropped.
2. **Revenue curve, net:** price × demand per 1,000 addressable customers, using **what you keep**. Remove VAT (UK consumer prices include 20%), the app-store or platform fee (15% or 30%) and the variable cost.
3. **Reconcile instruments.** If Van Westendorp/NMS says 28% would buy at £14 and Gabor-Granger says 62% (SYNTHETIC Fernhill), that 2× gap is a finding. Report both, and treat the gap as your uncertainty.
4. **Segments by maximum willingness to pay.** These show who you lose at each step up in price.
5. **Stated willingness to pay is optimistic.** Validate with a live price test or a fake-door test (see the `demand-test` skill) before you lock in a price.

## Step 4: Package design

Read `references/packaging.md`.

- **Good-Better-Best:** one price leaves money on the table above it and loses volume below it.
- **Fences** between tiers (usage limits, seats, features) must match how the segments actually differ.
- **Free/freemium:** if the free tier is generous enough, paid customers move down to it. Watch the downgrade-to-free rate.
- **Heavy users:** if cost-to-serve exceeds price, use a cap plus overage.
- Use TURF from the MaxDiff study to choose what goes in each tier.

## Step 5: Model and recommend

Read `references/report-template.md`. Recommend:

- launch price and tiers
- billing (monthly first, then annual). **The annual discount is a retention-economics decision, not a stated-intent threshold.** Compare 12 × monthly price × expected months retained against annual price × (1 − refund rate). A 20% discount pays only if monthly customers would stay fewer than about 9.6 of 12 months. Seasonal products (e.g. exam-year tutoring) churn on a calendar, so model that.
- a price-increase policy: maximum step size, and price-lock for early adopters
- a migration plan for existing customers: soft vs forced, by region, with a go/no-go date
- a risk register

Feed the price into the PR/FAQ external FAQ ("What does it cost?") and the internal FAQ (unit economics).

## Mistakes

1. Pricing from cost or from gut. Many founders under-price by 2–3×.
2. Treating the highest revenue index as the answer without checking the segment and adoption risk.
3. Testing without the real marketing claims in the stimulus.
4. Leading with technology labels. In one UK study, in a **multi-select "which of these would you pay more for?"** question (not MaxDiff), "AI-powered personalised learning" was picked by 7.3%, while outcome-worded features scored 44–55%. The wording sat at different levels of abstraction, so treat it as a messaging signal, not a ranking.
5. A free tier with no fence.
6. Quoting consultancy-scale confidence from a single-market n=200 panel.
7. Reading revenue off gross prices. VAT and store fees can cut what you keep by 30–45%.
