---
name: experiment-design
description: "Design, size, run and read A/B and multivariate tests properly: IF/THEN/DUE TO hypothesis, one pre-registered primary metric plus guardrails, minimum detectable effect, sample size and whole-week duration, sample-ratio-mismatch check, no peeking, novelty effects, MVT cell counts, feature flags and staged rollout (1%->5%->25%->100%) with rollback triggers, and what to do when traffic is too low. Use when the user asks to A/B test, split test, run an experiment, multivariate test, calculate sample size, read test results, roll out a feature gradually, or decide whether a test 'won'."
metadata:
  version: 0.1.0
---

# Experiment Design

Practice from a large subscription business:
- Every key journey was tested before rollout.
- Every hypothesis was written as IF / THEN / DUE TO.
- Results used p < 0.05 and 80% power, with each line labelled "significant" or "not significant".
- **Roll out where the metrics improved. Roll back where they got worse.**

Run `scripts/experiment_toolkit.py`.

## Step 1: Hypothesis
**IF** we [change], **THEN** [primary metric] will [rise/fall] by at least [MDE], **DUE TO** [the customer reason].

Example: IF we let visitors browse the content library before signing up, THEN visitor-to-paid conversion rises by ≥10% relative, DUE TO higher perceived value.

## Step 2: Pre-register (write it down before launch)
| Item | Example |
|---|---|
| Primary metric (one) | Visitor → paid within 7 days |
| Guardrails (2–3) | Refund rate; support contacts per 1,000; page load time |
| Baseline | 5.0% |
| MDE (relative) | 10% |
| α / power | 0.05 / 80% |
| n per arm | `sample_size_per_arm(0.05, 0.10)` = 31,234 |
| Duration | `duration_weeks(31234, 2, 20000)` = **4 whole weeks** |
| Stop rule | Fixed date. No peeking-and-stopping |

## Step 3: Check you have the traffic
If `low_traffic_advice()` says it would take more than about 6 weeks, **don't run the A/B test**. Instead:

- usability-test the change (5 × 3)
- run a fake door (`demand-test`)
- test a bolder change (a bigger MDE needs far less traffic; 20% needs about a quarter of the sample)
- measure a higher-traffic upstream step
- use a staged rollout with a holdout group, and accept weaker evidence

Most micro-teams are here.

## Step 4: Run safely
- Use a feature flag; hash users so each person always gets the same arm.
- Stage it: 1% for 24 h (catch bugs) → 5% for 2–3 days → 25% for a week (read it as the A/B) → 100% with a 5% holdout.
- Rollback triggers, set before launch: error rate > 0.5%, crash-free < 99.5%, or any guardrail past its pre-set limit in the test plan's units → flag off.
- **SRM check** on day 1 and at the end: `srm_check([n_a, n_b], [0.5, 0.5])`. p < 0.001 means the split is broken. Stop and fix the bug; don't read the results.
- Watch for novelty effects: compare week 1 with week 4.

## Step 5: Read and decide
`readout(conv_a, n_a, conv_b, n_b)` gives the lift, a CI on the difference, and p.

| Result | Decision |
|---|---|
| Primary significantly up, guardrails fine, SRM ok | **Roll out** (stage 25% → 100%, monitor for 2 weeks) |
| Primary significantly down, or a guardrail broken | **Roll back** |
| Not significant | No effect at this MDE. Keep the simpler version, or iterate a bolder idea |

**Multi-market:** read each market separately. A win in one market and a flat result in another is a valid outcome, e.g. roll out in DE, iterate in IT.

## MVT
A full factorial multiplies the arms: 2 × 3 × 2 = 12 cells, so each cell gets 1/6 of the traffic an A/B arm would. Only use MVT on very high-traffic pages. Otherwise, run sequential A/B tests.

## Output
A one-page test plan before launch, and a one-page readout after it. Template: hypothesis · pre-registration table · SRM · results by metric and market (significant or not) · decision · next test.
