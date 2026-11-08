# Worked example (SYNTHETIC: Stridewell, fictional home-workout app, 90 days after launching "Daily Workout")

| Metric | Success | Watch | Kill | Actual (day 90) | Decision |
|---|---|---|---|---|---|
| Activation: first workout in 24h | ≥ 55% | 40–55% | < 40% | 61% | ✓ success |
| Week-4 retention | ≥ 35% | 25–35% | < 25% | 29% | watch → iterate |
| Paid conversion by day 30 | ≥ 6% | 4–6% | < 4% | 4.4% | watch → iterate |
| Involuntary churn (failed payments) | ≤ 1.5% / mo | 1.5–3% | > 3% | 2.6% | watch → dunning fix |

## Churn staircase for the next quarter
Monthly churn 8.0% → target 6.5%:

| Lever | Group | Churn pts | RAG |
|---|---|---|---|
| Smart retries + dunning SMS | Prevent | −0.6 | Green |
| Reminder at the user's usual workout time | Engage | −0.5 | Amber (needs an A/B test) |
| Pause for 1 month in the cancel flow | React | −0.3 | Green |
| Win-back email at day 30 with a free week | React | −0.2 | Amber |
| **Total** | | **−1.6** (to 6.4%) | |

**Decision:** iterate. Ship dunning and pause first: low effort, high confidence.
