# Governance templates (SYNTHETIC examples: Parcelpoint, a fictional parcel-locker app)

## Weekly squad update
| # | Initiative | Summary (dated) | Sponsor | Owner | Stage | Due | RAG |
|---|---|---|---|---|---|---|---|
| 1 | Locker reservation | 06/11: NO CHANGE. In beta with 3 sites | Ops Director | PM, Lockers | Delivery | 28/11 | Green |
| 2 | Courier API v2 | 06/11: partner sandbox down 4 days; asked their CTO for an SLA | Partnerships | PM, Platform | Delivery | 05/12 | Amber |
| 3 | Returns QR flow | 06/11: legal review of terms blocked; options paper attached | Legal | PM, Returns | Shape | 12/12 | Red |

**Stages:** Pre-planning → Prioritised → Shape → Delivery → Completed. Write "NO CHANGE" when nothing moved; that's honest, not lazy.

## WBR callout (one per out-of-range metric)
> **Metric:** Locker pickup within 24h, **71%** (normal range 78–86%)
> **Hypothesis:** the Leeds sites' SMS provider failed on Tue–Wed. 2,300 notifications were delayed.
> **Evidence:** delivery-receipt rate fell from 99% to 61% on those days.
> **Action:** switch to the backup provider (owner: Platform PM, Fri). Add an alert when receipts drop below 95%.

## Quarterly alignment agenda (90 min)
| Block | Time |
|---|---|
| Last quarter: goals hit and missed, with the metric for each | 20 |
| More of / less of / speed up / slow down | 20 |
| Proposed quarter: RICE+ table, the cut line, what we are NOT doing | 30 |
| Decisions and DACI for anything that crosses squads | 20 |

## DACI register
| Decision | Driver | Approver (one) | Contributors | Informed | Date |
|---|---|---|---|---|---|
