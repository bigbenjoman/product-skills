---
name: maxdiff-study
description: "Design, field and analyse a MaxDiff (best-worst scaling) study to decide which features, benefits or messages to build or lead with. Use when the user mentions MaxDiff, best-worst scaling, feature prioritisation survey, 'which features matter most', ranking a backlog with customers, or wants customer evidence for a PR/FAQ backlog or RICE score. Covers the decision brief, item writing, experimental design, questionnaire, Prolific recruitment and costing, analysis (counts, logit utilities, share of preference, segment cuts, TURF) and a decision-ready report. Not for setting a price: hand off to pricing-study."
metadata:
  version: 0.1.0
---

# MaxDiff Study

MaxDiff shows a respondent a small set of items, usually 4, and asks for the **most** and **least** important. Repeated across balanced sets, this forces trade-offs that rating scales never do. On a 1–5 scale everything is "important". In MaxDiff, something has to lose.

A study that a consultancy would charge tens of thousands for can be run by one person in a week for a few hundred pounds of panel cost. This skill does the expert parts. The human does the judgement parts.

## Step 0: Start from the decision (Working Backwards)

Before writing an item, write down:

1. **The decision this study will change.** For example: "which 5 of 14 backlog items go into the launch MVP", or "which benefit leads the press release headline".
2. **What you will do for each plausible result.** If every outcome leads to the same action, do not run the study.
3. **Who the customer is**, specifically enough to write a screener for.
4. **Which segments must be compared.** Each segment you intend to cut needs roughly 100+ completes.

If a PR/FAQ exists (see the `working-backwards` skill), read it first. The backlog in its appendix is the usual item source.

## Step 1: Write the items

Read `references/item-writing.md`. Rules in brief:

- **8–30 items.** 12–20 is the sweet spot.
- **One idea per item**, written in customer language, at the same level of abstraction.
- **Outcomes over technology labels.** In one UK pricing survey (a multi-select "would pay more for" question, not MaxDiff), "AI-powered personalised learning" got 7.3% while outcome-worded features got 44–55%. Label the outcome, not the mechanism, and keep every item at the same level of abstraction.
- No double-barrelled items ("fast and cheap"). No near-duplicates.
- Items must be things you could actually ship. Do not test fantasies.

Show the item list to the user and get sign-off before the design step.

## Step 2: Build the experimental design

Run `scripts/maxdiff_toolkit.py`. Call `design(n_items, per_set, n_sets, n_versions)`.

- `per_set`: 4. Use 5 for 20+ items. Never more than about half the item count.
- `n_sets`: aim for each item to be seen **at least 3 times** per respondent, so `n_sets ≈ 3 × n_items / per_set`. For example, 12 items in sets of 4 gives 9 sets.
- `n_versions`: 5–10. The generator randomises item position within each set and the set order in each version, and it balances pair co-occurrence across all versions.
- Check the output. Every item should appear the same number of times, every item should appear in every position (roughly evenly), and pair co-occurrence should be within a narrow band (e.g. 5–11 for 12 items × 10 versions).
- `export_design_csv(versions, items, path)` writes the design to load into your survey tool.

## Step 3: Write the questionnaire

Read `references/questionnaire-template.md`. Order:

1. **Screener.** Qualify the customer defined in Step 0. Disqualify early.
2. **Stimulus.** A short description or a 60-second product video. **Every respondent sees the same stimulus.** Anything left out of the stimulus is not priced into the answers.
3. **MaxDiff tasks.**
4. **Anchor question** (dual response, strongly recommended). "Would you consider any of these essential?" or a per-item yes/no on the top items. Plain MaxDiff is *relative*: the winner of a weak list is still weak. The anchor tells you whether anything clears the bar.
5. **Optional Kano pair** on the top 6–8 items: "How would you feel if it had X / did not have X?" (Like / Expect it / Neutral / Can live with it / Dislike). Classify with `kano_classify()` and summarise with `kano_summary()`, which gives the category and the Better/Worse coefficients. MaxDiff gives forced importance; Kano gives the *shape* of satisfaction. They are different questions. See `references/kano.md`.
6. **Segmentation and profile questions.**
7. **Two attention checks.**

## Step 4: Recruit and cost it

Default panel: **Prolific** (UK/US consumers and many professional screeners). B2B decision-makers are harder to reach; see `references/fielding.md`.

Cost formula, which you must show to the user:

```
cost = completes × reward per complete × (1 + platform fee rate) + survey tool licence
```

- **Reward per complete:** Prolific enforces a minimum hourly rate. A benchmark from a real 2026 UK consumer study: a 4.5-minute median survey paid **£1.80–£2.00 per respondent**.
- **Platform fee rate and tool licence:** check the *current* figures on Prolific's and the survey tool's pricing pages before quoting a number. Never quote a fee from memory.
- **Sample:** 200 completes minimum, plus about 100 per segment you plan to cut. Add 10–15% for quality exclusions.

## Step 5: Analyse

Load choices with `load_responses_csv(path)` (columns: resp, segment, set_items, best, worst). Then run `analyse(responses, n_items)`. Worst is modelled sequentially by default: worst is chosen from the set *minus* the best item. It returns:

- **Count scores:** (best − worst) / times shown, a range of −1 to +1. Transparent, and good enough for most decisions.
- **Logit utilities**, using an aggregate multinomial logit model.
- **Share of preference (0–100):** easiest for stakeholders to read.

Also run:

- `bootstrap_ci()` for 95% intervals. Two items whose intervals overlap are a tie, not a ranking.
- `segment_cuts()` for each segment.
- `anchor_share()` for the % of respondents who said they would pay for, or need, each item.
- `turf(anchors, n_items, k)` for the best k-item bundle.

For individual-level utilities (Hierarchical Bayes), use the survey tool's built-in analysis (Conjointly, Sawtooth, Qualtrics).

Always produce:

1. The ranked chart with share of preference.
2. **Segment cuts**: where segments disagree is often the real insight.
3. The **anchor line**: which items clear the "essential" bar.
4. **TURF** (if building tiers or bundles): the smallest set of items that gives the most respondents at least one item they love.

## Step 6: Make the decision

Read `references/from-results-to-roadmap.md`.

- Use MaxDiff as evidence for **one** RICE+ factor only: **Impact**, as share of preference banded to the scale. Take **Reach** from behaviour or the market (how many customers the feature touches), not from the same survey. Taking both from MaxDiff counts the same preference twice. Anchor % and sample size set **Confidence**, which is capped at 80% for stated preference until you see behaviour.
- Research **informs** prioritisation; cost, strategy and constraints **decide** it. State explicitly where you overrode the ranking and why.
- Items with high importance but low anchor are messaging opportunities, not build opportunities.
- Update the PR/FAQ: the top item usually belongs in the headline or the first paragraph.

## Output

Use `references/report-template.md`: a one-page decision memo first, with the charts and method in an appendix. State n, dates, panel, exclusions and design. Label any simulated or illustrative data as **SIMULATED** on every chart.

## Common mistakes

1. Treating relative importance as absolute. Fix this with the anchor.
2. Testing jargon or technology labels instead of outcomes.
3. Surveying only existing users. Their answers are biased towards the product you already have.
4. Different stimulus for different respondents.
5. 40 items in sets of 6: respondent fatigue, and noise.
6. Reporting the ranking without the decision it changes.
