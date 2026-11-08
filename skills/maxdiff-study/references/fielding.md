# Fielding

## Panels
- **Prolific:** best default for UK/US consumers and screened professionals. Fast (often under 48h for n=200), high attention-check pass rates. Benchmark from a 2026 UK parent study: £1.80–£2.00 reward per respondent for a ~4.5-minute survey, and 100% attention-check pass.
- **B2B decision-makers:** expensive and slow on any panel. Options:
  - your own customer and prospect list (biased, but cheap)
  - LinkedIn outreach with an incentive
  - specialist B2B panels
  - a CATI-validated vendor sample (used by pricing consultancies for n≈500 cross-market studies; budget accordingly)

## Tools
- **Conjointly:** MaxDiff, Van Westendorp, Gabor-Granger, conjoint, with built-in HB and Prolific integration
- **Sawtooth (Lighthouse / Discover):** the reference implementation for MaxDiff and conjoint
- **Qualtrics:** an enterprise MaxDiff module
- **OpinionX:** lightweight ranking and pairwise
- **DIY:** forms tool plus `maxdiff_toolkit.py`. Fine for counts and aggregate logit. No HB.

Always check current pricing on the vendor's site before quoting a cost to anyone.

## Quality
Exclude:
- speeders (under 50% of median time)
- straight-liners
- failed attention checks
- contradictory screener answers

Report exclusions.
