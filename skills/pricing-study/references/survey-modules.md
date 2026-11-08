# Survey modules

## Van Westendorp (after the stimulus)
1. At what price would you consider [product] to be so expensive that you would not consider buying it? (Too expensive)
2. At what price would you consider it expensive, but still worth considering? (Expensive)
3. At what price would you consider it a bargain, a great buy for the money? (Cheap)
4. At what price would it be so cheap that you would question its quality? (Too cheap)

**NMS extension:** "At [their cheap price] / [their expensive price], how likely are you to buy?" (5-point scale).

Calibrate the answers before using them. Stated likelihood overstates purchase. Default weights: 5 → 0.7, 4 → 0.3, 3–1 → 0. These are an assumption, so state them. Then interpolate between each person's two prices and average. `nms_curves()` does this.

**Validation:** too cheap < cheap < expensive < too expensive. Drop or repair anyone who violates the order.

## Gabor-Granger (adaptive)
"Would you buy at £X?" Ask about 5 points drawn from the Van Westendorp range. Go up after a yes and down after a no.

**Analysis:**
1. Record each respondent's **maximum accepted price**. Use "none" if they said no at every price.
2. demand(p) = the share of ALL respondents whose maximum is at least p.
3. Revenue index = p × demand(p), using net price where it matters.

Never divide the yeses at a price by the number of people shown that price. In an adaptive ladder, only earlier yes-sayers reach the high prices, so that number is inflated.

**Worked correction (SYNTHETIC: Fernhill Coffee, n=200).** Segment shares by maximum price: £18 18%, £16 10%, £14 34%, £12 8%, £10 14%, none 16%.

| Price | Demand | Revenue index |
|---|---|---|
| £10 | 84% | 8.40 |
| £12 | 70% | 8.40 |
| **£14** | **62%** | **8.68 (max)** |
| £16 | 28% | 4.48 |
| £18 | 18% | 3.24 |

The "shown-base" method tends to make the top price look like the revenue winner. That is the artefact.

## Monadic cells
Randomly assign each respondent ONE price: −50 / −20 / 0 / +20 / +50% of the reference price. Volume index and revenue index per cell, and arc elasticity between neighbouring cells.

**Watch for psychological thresholds.** A small rise across one (£9.99 → £10.49) can lose revenue. If you cross a threshold, go to the next one.

## Interest × WTP (per item)
- Interest: 1–4
- "If this were only available by paying extra, how likely would you be to pay?" 1–4

Plot as quadrants: Hero (high/high), Niche (low interest, high pay), Nice-to-have (high interest, low pay), Lower value (low/low).

## Pricing-power scorecard (existing customers)
Rate each indicator high/neutral/low, then combine:
- value-for-money agreement
- NPS
- **price recall accuracy**: if customers know the price, they will notice a change
- % who say the current price is expensive

## Billing and evolution
- Monthly vs annual vs "depends on the discount"
- Cumulative uptake by annual discount level (10/15/20/25/>25%). Look for the jump.
- Price-increase tolerance (+£1/+£2/+£3/+£5): continue / continue but less happy / consider cancelling / cancel. Look for the cliff.
- Grandfathering expectation: permanent / 12 months / loyalty discount / accept the new price for new features
