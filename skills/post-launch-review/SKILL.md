---
name: post-launch-review
description: "Run the post-launch phase: 30/60/90-day reviews against success/watch/kill criteria set before launch, activation and onboarding (aha moment, time to first value), the churn programme (Prevent / Engage / React: payment failure and dunning, engagement levers, cancellation flow, pause, save offers, win-back), quality targets set from customer verbatims, iterate / kill / sunset decisions, deprecation playbooks with customer comms, and incident severity S1-S4 with post-mortems. Use when the user asks what to do after launch, post-launch review, retention or churn, onboarding, activation, cancellation flow, win-back, dunning, sunsetting or deprecating a feature, incident severity or post-mortem."
metadata:
  version: 0.1.0
---

# Post-Launch Review

Launch is the start of the evidence, not the end of the project.

## 1. The 30/60/90 review (against criteria set BEFORE launch)
| Day | Question | Typical metrics |
|---|---|---|
| 30 | Are people getting value? | Activation rate, time to first value, S1/S2 incidents, support contacts per 1,000 |
| 60 | Are they coming back? | Week-4 retention, visit days, usage of the core feature |
| 90 | Is it paying? | Paid conversion, churn, net revenue vs plan |

For each metric: success / watch / kill threshold → actual → **decision**. Never move a threshold after launch without writing down why.

## 2. Activation and onboarding
1. Define the **aha moment** as the action most linked to retention (from `metrics-and-wbr`). Example: "first call answered and booked".
2. Measure time to first value.
3. Remove every step between sign-up and aha that isn't legally or technically required. Ask for the rest later.
4. Test onboarding changes with `experiment-design`, or `usability-test` if traffic is low.

## 3. Churn programme: Prevent / Engage / React
| Lever group | Levers | Metric |
|---|---|---|
| **Prevent** | Payment failure: card updater, smart retries, **dunning** emails and SMS, in-app "update card" prompt | Involuntary churn % |
| **Engage** | Habit features linked to retention (reminders, personalisation); quality fixes from verbatims | Visit days, retention by cohort |
| **React** | Cancellation flow: reason survey, **pause** option, a save offer matched to the reason, easy cancel; win-back at 30/90 days | Save rate, win-back rate |

Size each lever in churn points and £, colour it RAG, and stack them into a churn staircase (`prioritise-roadmap`).

**UK rules:** cancelling must be as easy as signing up. Check the current status of the DMCC Act subscription-contract rules before you design the flow. No confirmshaming.

## 4. Quality targets from customer pain
Turn verbatims into measurable targets. Example pattern from live streaming:
- "It freezes during the match" → rebuffering from 1% to under 0.4%
- "Goals arrive on my phone first" → latency from over 1 minute to 20 seconds or less

Then track those targets on the WBR.

## 5. Iterate, kill or sunset
- **Iterate:** watch-zone metrics with a clear hypothesis.
- **Kill:** below the kill threshold, with no credible hypothesis left.
- **Sunset (deprecation playbook):**
  1. Decide the date.
  2. Warn in-product 30–60 days ahead.
  3. Email affected customers with the alternative.
  4. Offer a migration path or compensation where fair (e.g. a voucher for unsupported old devices).
  5. Monitor forums and support.
  6. Remove the feature, then confirm metrics and support load.

## 6. Incidents: severity and post-mortems
| Sev | Definition (adapt the thresholds to your product) |
|---|---|
| S1 | Core journey down for many users (sign-up, playback, booking) for more than a few minutes, or any outage during a showcase moment |
| S2 | Core journey degraded for a segment, or a showcase feature partly down |
| S3 | Minor or short-lived impact |
| S4 | Everything else, including issues you spotted and avoided |

Post-mortem template: `references/post-mortem.md`. Blameless; five whys; action items with owners; fix the process that allowed it.

## Worked example
`references/worked-example.md`
