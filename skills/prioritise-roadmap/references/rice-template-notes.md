# RICE+ template notes
- One `mode` per scoring round. Don't rank `gbp` rows against `scale` rows. Split them into two tables, or convert everything to £.
- `effort` = build days + review hours ÷ 6 (one review day ≈ 6 focused hours).
- `score`:
  - scale mode = reach × impact × confidence ÷ effort
  - £ mode = impact_gbp × confidence ÷ effort (no Reach)
- Sort overrides first, then by score. `cumulative_effort` runs down the sorted list. Set a named cell `CAPACITY`.
- Staircase per row: quarterly £ = base × uplift × ramp(q) × confidence.
