# Behavioural analytics: method and worked example

## 1. Definitions first (write them in the doc)
- **Cohort:** accounts grouped by start month.
- **Retained at month N:** has an active paid subscription on day 30×N after start.
- **Early window:** days 0–30 after start. All behaviour inputs are measured here.
- **Censored:** accounts younger than 30×N days are excluded from month-N rates. They are not churned. They are unknown.

## 2. Worked SQL (Postgres; SYNTHETIC schema for Stridewell, a fictional home-workout app)
```sql
-- accounts(id, started_at, market), sessions(account_id, started_at), subscriptions(account_id, active_on date)
with early as (
  select a.id, a.market,
         count(distinct date(s.started_at)) as visit_days_0_30
  from accounts a
  left join sessions s on s.account_id = a.id
       and s.started_at < a.started_at + interval '30 days'
  group by a.id, a.market
),
banded as (
  select *, case when visit_days_0_30 >= 14 then '14-30'
                 when visit_days_0_30 >= 8  then '8-13'
                 else '1-7' end as band
  from early
),
outcome as (
  select b.*, a.started_at,
         exists (select 1 from subscriptions x where x.account_id = b.id
                 and x.active_on = date(a.started_at + interval '90 days')) as retained_m3
  from banded b join accounts a on a.id = b.id
  where a.started_at + interval '90 days' <= current_date      -- censoring: only accounts old enough
)
select market, band, count(*) as accounts,
       round(100.0 * avg(retained_m3::int), 1) as pct_retained_m3
from outcome group by market, band order by market, band;
```

## 3. Worked result (SYNTHETIC)
| Market | Visit days 0–30 | Accounts | Retained at M3 |
|---|---|---|---|
| UK | 1–7 | 4,120 | 38.2% |
| UK | 8–13 | 2,310 | 51.0% |
| UK | 14–30 | 1,480 | 63.5% |

**Reading it:**
- 14–30 against 1–7 is +25.3 points **absolute**, about +66% **relative**. Always say which one you mean.
- **Next steps:**
  1. Hold minutes exercised constant: band by minutes too, and compare within each band.
  2. Check the confounder: are 14–30 users more often on paid plans from day 1?
  3. Form the hypothesis: "daily reminders that raise visit days will raise M3 retention".
  4. Test it (`experiment-design`). Correlation tells you where to look. The experiment tells you if it's true.

## 4. Engagement funnel template
| User need | Customer action | Measure | Feature examples |
|---|---|---|---|
| "Remind me to work out" | Visit | Visit days / week | Push reminder at the user's usual time |
| "What should I do today?" | Start a workout | Workout starts | Home screen "next workout" card |
| "Keep me going" | Finish a workout | Completion % | Streaks, shorter workouts |
| "What else?" | Start another | Workouts per visit | Autoplay next workout |
