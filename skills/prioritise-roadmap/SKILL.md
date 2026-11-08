---
name: prioritise-roadmap
description: "Turn customer evidence, MaxDiff/Kano results and commercial estimates into a prioritised, defensible roadmap using RICE+ (Reach, Impact in ONE unit per scoring round, Confidence capped for stated preference, Effort including human review/decision hours, plus written overrides for contractual, regulatory, competitor-gap, broken-UX and Kano must-be factors), a capacity cut line, revenue and churn staircases (base x uplift x ramp x probability), a programme plan and a draft strategy narrative. Use when the user asks to prioritise a backlog, build a roadmap, score features, decide what to build next, RICE, or justify product investment to a board."
metadata:
  version: 0.2.0
---

# Prioritise the Roadmap (RICE+)

This is Ben Lavender's annual product-strategy cycle: **Gather → Shape → Approve → Deliver**, repeated yearly or sooner. This skill does the **Shape** step.

## Inputs (ask for anything missing)
- **Business targets:** revenue, EBITDA, churn, by market or segment.
- **Customer evidence:** from `customer-evidence`. MaxDiff and Kano results from `maxdiff-study`.
- **Competitor matrix:** from `market-analysis`.
- **Effort estimates:**
  - engineering days (S/M/L mapped to ranges is fine)
  - **human review and decision hours**, which are the binding constraint when agents build
- **Commitments:** contractual, regulatory and partner deadlines.
- **Capacity for the period:** e.g. "120 build-days and 60 review hours this quarter".

## Step 1: Pick ONE impact unit for this scoring round
Mixing units in one ranking makes the scores meaningless. Choose one:

- **£ mode:** Impact = 12-month (or 3-year) incremental contribution in £, from a commercial estimate. **Do not multiply by Reach.** The £ figure already contains how many customers it touches.
  - Score = Impact £ × Confidence ÷ Effort.
- **Scale mode:** use this when there's no credible £ estimate.
  - Reach = customers touched in 12 months, from usage data or the market. **Never take this from the same survey as Impact.**
  - Impact = 3 / 2 / 1 / 0.5 / 0.25, where 3 is massive and 0.25 minimal (MaxDiff share of preference, banded, is good evidence here).
  - Score = Reach × Impact × Confidence ÷ Effort.

## Step 2: Confidence (honest about evidence)
| Evidence | Confidence |
|---|---|
| Live behaviour: A/B result, fake-door rate, usage data | 100% |
| Stated preference with n≥200, anchored, CIs separate | 80% (the cap for surveys) |
| Small survey, interviews, usability findings | 50% |
| Opinion or HiPPO (the highest-paid person's opinion) | 20–30% |

## Step 3: Effort
- **Effort = build days + review/decision hours ÷ 6.**
- When agents write the code, build days shrink and **review hours dominate**. Estimate both and add them.

## Step 4: Overrides (+ factors), each written down
These can move an item above the line regardless of its score:

- contractual or regulatory commitment
- P1 competitor gap (customers name it and every competitor has it)
- broken UX
- Kano **must-be** (build to parity)
- strategic bet

**Write one sentence per override.** Accessibility is a legal duty (Equality Act 2010; European Accessibility Act, in force June 2025). Treat it as an override, not a low-impact nice-to-have.

## Step 5: Capacity cut line
1. Sort by score, keeping overrides at the top.
2. Add up effort down the list until you hit capacity. Draw the line there.
3. Everything below the line is "not this period". Say so out loud.

**Ben's rules:**
- Initiatives that work across many brands or markets earn more Reach.
- Prefer fewer initiatives.
- Take the quick wins.
- Use the **5-step rebalance:**
  1. Shortlist about 20 with an initial RICE score.
  2. Survey a statistically sound sample per market.
  3. Rebalance RICE with the customer ranking.
  4. Take the quick wins.
  5. Prefer fewer initiatives.

## Step 6: Staircases (the money view)
Per initiative: **incremental revenue per quarter = base × uplift × ramp × probability.**

| Term | Meaning |
|---|---|
| base | revenue (or customers) the change acts on |
| uplift | expected % change (e.g. conversion +3%) |
| ramp | 0 → 1 over the rollout quarters (e.g. 0.25, 0.75, 1) |
| probability | the confidence from Step 2 |

- Stack the initiatives on top of the base business by quarter to get the **revenue staircase**.
- Do the same for churn points to get the **churn staircase**, grouped Prevent / Engage / React.
- Colour each step RAG by delivery risk. Total the £ at risk from red and amber.

## Outputs
1. Ranked table, using `references/rice-template.csv`:
   initiative · metric targeted · R · I · C · E (build + review) · score · override reason · above or below the line · quarter
2. Revenue staircase, and optionally a churn staircase.
3. **Draft strategy narrative**, up to 6 pages of prose: context; tenets; what we will do; what we will NOT do and why; risks; FAQ.
4. **Approve pack:** trade-offs, budget and resource flags, and what each stakeholder loses. No surprises.

## Rules
- Research **informs**; it does not decide. A 60% customer-vote feature can rank P1 while a 70% one ranks P3, because of cost or strategy. That is legitimate **only if the reason is written down**.
- Every initiative above the line needs a PR/FAQ before build (`working-backwards`). Most should die there.
- Map each initiative to the **input metric** it moves (`metrics-and-wbr`). If it maps to no metric, ask why it exists.
