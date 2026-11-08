---
name: governance-cadence
description: "Design and run product governance: squads aligned to the customer journey (e.g. Growth, Partnerships/Distribution, Playback/Core experience, Engagement, Quality, Analytics & Experimentation), the weekly squad update (RAG per initiative), weekly programme review, Weekly Business Review, quarterly roadmap alignment, DACI decision roles and the annual strategy refresh with course-correction (more of this / less of that, speed up / slow down). Use when the user asks how to organise product teams, set up squads, run a WBR, weekly status reporting, roadmap reviews, QBRs, operating cadence or decision rights."
metadata:
  version: 0.2.0
---

# Governance Cadence

Governance is how a strategy survives contact with the week. Keep it light: every meeting must change a decision, or it goes.

## 1. Squads aligned to the customer journey
- Map the customer journey from discover through join, use and return to renew. Give each stage, or a cluster of stages, one cross-functional squad: product, UX, engineering, data, plus a named business sponsor.
- Example structures:
  - Streaming at global scale: Growth, Partnerships, Playback, Engagement, Ads & Media, Machine Learning, Operating Tools.
  - Converging a platform: Distribution, Growth, Playback, Engagement, Quality, Analytics & Experimentation.
- Each squad has:
  - a mission line
  - 1–2 input metrics it owns
  - a single-threaded product lead

## 2. The cadence
| Ritual | When | Who | Output |
|---|---|---|---|
| Weekly squad update | Weekly, written | Each squad | Table: initiative, summary, business sponsor, product owner, delivery lead, stage, due date, RAG |
| Weekly programme review | Weekly, 45 min | Leads + stakeholders | Only the critical subset of initiatives; decisions and escalations |
| Weekly Business Review | Weekly, 60 min | Metric owners | Consistent charts; callouts outside normal range, each with a hypothesis and a remediation |
| Quarterly roadmap alignment | Quarterly | Each squad + stakeholders | Agreed squad strategy and goals for the quarter |
| Annual strategy refresh | Annually, or sooner | Leadership | Gather → Shape → Approve → Deliver, again |

## 2b. RAG definitions (use these exact rules)
| RAG | Rule |
|---|---|
| **Green / On track** | Will hit the due date and scope with current people. No help needed |
| **Amber / At risk** | Will miss the date or scope by under 2 weeks **unless** a named action happens. Ask for the help |
| **Red / Off track** | Will miss by 2+ weeks, or a decision is blocked. Escalate this week, with options |
| **Completed** | Live with customers, and metric tracking confirmed |

Call amber before it turns red. A culture where everything is green until it's red is one where nobody trusts the update.

## 2c. Micro-team variant (2–5 people): two rituals and an agent-written update
| Ritual | When | How |
|---|---|---|
| **Monday written update** | Weekly, automated | An agent drafts it from tickets, commits and blockers. A human edits it in 10 minutes |
| **WBR + priorities** | Monday, 45 min | The metrics outside normal range, each with a hypothesis; then the week's three priorities and the more-of / less-of lists |
| **Demo and decide** (optional) | Thursday, 30 min | Demo what shipped to customers; take one or two DACI decisions; kill or continue anything stuck |

Add quarterly roadmap alignment once you have external stakeholders (investors, partners).

Templates: `references/templates.md`.

## 3. Course-correction
Every quarter, write four lists:
- **more of this**
- **less of that**
- **speed up**
- **slow down**

Each list item needs the metric or evidence behind it.

## 4. Decision rights (DACI)
For each cross-squad decision, name one **D**river, one **A**pprover, the **C**ontributors and who is **I**nformed. Two approvers means no approver.

## Outputs
1. Squad map: missions and the metrics each squad owns
2. Templates for the weekly update, programme review and WBR
3. Quarterly alignment agenda
4. DACI register
