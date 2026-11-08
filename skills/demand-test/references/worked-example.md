# Worked example (SYNTHETIC: Fernhill Coffee, fictional coffee subscription)

**Question:** should we build annual billing at 20% off?

**Decision rule, set beforehand:**
- Build if ≥15% of plan-page visitors click "Pay annually".
- Drop if <8%.

**Why 15%?** At 15% uptake and 20% off, annual revenue breaks even against expected monthly churn. See the pricing module.

**Sample:** `n_for_margin(0.15, 0.035)` gives about 400 plan-page visitors. At about 200 visitors a day, that's 2 days. Run 14 days to cover two full weeks.

**The door:** a "Pay annually: save 20%" toggle on the plan page. On click: "Annual billing is coming soon. You're on monthly for now, and nothing has changed. Want us to email you when it's ready? [Yes, email me]". The email box is **unticked**.

**Result:**
- 412 visitors, 74 clicks, giving **18.0%**.
- Wilson 95% CI: **14.6% – 22.0%**.
- 31 asked to be emailed.

**Read:**
- The point estimate (18.0%) clears 15%.
- The interval's lower end (14.6%) does not, quite.
- **Decision:** iterate. Run 7 more days to narrow the interval. If the lower bound clears 15%, build.

**After 21 days:**
- 640 visitors, 118 clicks, giving 18.4% (CI 15.6% – 21.6%).
- **Build.** Remove the door on the day annual billing ships, and email the people who opted in.
