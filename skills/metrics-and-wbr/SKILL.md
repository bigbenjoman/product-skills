---
name: metrics-and-wbr
description: "Behavioural analytics and metrics for a product: correlate input metrics to output metrics (retention, revenue), cohort survival curves, engagement funnels, targeting features at the metrics that matter, plus the metrics that tell you whether a launch is working and run them weekly: north-star and output metrics, controllable input metrics, a metric tree, launch success and kill criteria, A/B rollout/rollback rules, cohort retention analysis and an Amazon-style Weekly Business Review (WBR) pack. Use when the user asks what to measure, KPIs, north star, input vs output metrics, WBR, launch dashboard, success criteria, kill criteria, cohort or churn analysis."
metadata:
  version: 0.2.0
---

# Metrics, Behavioural Analytics and the Weekly Business Review

You cannot move output metrics (revenue, subscribers, profit) directly. You move the **controllable inputs** that cause them. The job here is to find which inputs actually cause your outputs, and then review them every week.

## Step 1: Metric tree
1. Name 1–2 output metrics. Example: paid subscribers retained at month 3.
2. Break each one into candidate inputs the team controls. Examples: days visited per month, time to first value, sign-up completion %, playback start time.
3. **Test the link with data** wherever it exists. Example from a real cohort analysis: users who visited 14–30 days a month were 10–25% more likely to be retained than those visiting 1–7 days, *at the same viewing hours*. Visit frequency, not volume, was the input to manage.
   - Before launch there is no data. Use proxy evidence and label each link as a **hypothesis**.

## Step 1b: Behavioural analytics (existing products)
Read `references/behavioural-analytics.md` for the full method and a worked SQL example. In order:
1. **Define retention exactly.** Example: "an account is retained at month N if it has an active paid subscription at day 30×N after its start date". Write this down before you query anything.
2. **Measure behaviour in a fixed early window, outcome after it.** Example: visits in days 0–30, retention at day 90. If you measure behaviour over the whole lifetime, people who stay longer automatically have more visits. That is survivorship / immortal-time bias, and it creates fake correlations.
3. **Correlation scan.** For each candidate input in the early window, compare retention between bands (e.g. 1–7, 8–13 and 14–30 visit days). Do this by market and segment, because links vary.
4. **Cohort survival curves.** Hold one variable constant to isolate another. Example: compare visit frequency at *equal* viewing hours. Treat accounts that haven't reached month N yet as **censored**: leave them out of month N, don't count them as churned.
5. **Check confounders.** Do frequent visitors differ in another way, e.g. league followers versus one-off event buyers? Split by that and look again.
3. **Engagement funnel.** Map visitor → sign-up → first value → habit → paid → retained. Find the step with the biggest drop that the team can control.
4. **Target features at metrics.** List each candidate feature against the input metric it moves. Any feature with no metric goes back to the backlog.
These findings feed Impact in RICE+ (see the `prioritise-roadmap` skill).

## Step 2: Launch criteria (write them before launch)
| | Example |
|---|---|
| Success | ≥ X% of trial users reach first value within 7 days |
| Watch | Sign-up conversion within ±10% of forecast |
| **Kill / rethink** | Fewer than Y paying after Z weeks at £__ marketing spend |

Kill criteria set before launch protect the team from sunk-cost reasoning afterwards.

## Step 3: Experiment rules
Use the `experiment-design` skill. The rule:

- **Before the test:** pre-register ONE primary metric (ideally the output, or an input with a proven link), 2–3 guardrails (e.g. refunds, support contacts, page speed), the MDE, the sample size and the stop date. Run whole weeks only.
- **Ship** only if all of these hold:
  - the primary metric beats control at the stated significance level
  - no guardrail is harmed
  - the sample-ratio-mismatch check passes
  - nobody stopped early because the numbers looked good ("peeking")
- **Roll back** if the primary metric is significantly worse or a guardrail breaks.
- "The input metric went up" is not enough on its own. Inputs can rise while the output falls (Goodhart's law).

## Step 4: The WBR pack (weekly)
- Follows the customer journey end to end: acquisition → activation → engagement → monetisation → retention → service
- Every chart shows **trailing 6 weeks and trailing 12 months** side by side, with prior year where it exists
- Add an exception report and 2–3 customer anecdotes.
  - **Normal range** = trailing 12-week mean ± 2 standard deviations (or control limits if you use SPC).
  - Seasonal metrics compare against the same weeks last year.
  - Every exception carries a written **hypothesis** and a named owner.
- **Meeting:** each metric owner explains variances only. "Don't know yet, back next week" is an acceptable answer. No strategy debates here.

## Step 5: Build the WBR with agents (no BI tool, no data team)
Running in production at a two-person start-up and at scale (100+ metrics). The short version:

1. PR/FAQ for the warehouse.
2. Metrics taxonomy. A micro-team marks **10–15 metrics as Now**.
3. An agent maps each metric to its source table.
4. Nightly sync into a separate analytics database, then dbt staging → intermediate → marts.
5. Daily pipeline, which stops on failure and shows "data is stale".
6. **One** metric registry for targets and RAG.
7. Portal: 6 weeks next to 12 months, prior year overlaid, callouts, RAG.

Builder detail: `references/wbr-build.md`.

## Outputs
1. The metric tree (diagram plus table)
2. Launch success, watch and kill criteria
3. Experiment plan
4. WBR template, with the chart list and an owner per metric
5. Optional: a metrics taxonomy, a warehouse spec and a build plan for an agent-built WBR (Step 5)
