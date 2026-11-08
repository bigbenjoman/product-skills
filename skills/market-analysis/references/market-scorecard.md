# Weighted market scorecard: worked example (SYNTHETIC; Oakbill, fictional invoicing and payments SaaS)

## Step 1: Raw indicators
| Market | Target firms | Avg software spend £/yr | English-language (1/0) | Partner reach (0–10) |
|---|---|---|---|---|
| UK | 9,800 | 1,900 | 1 | 8 |
| Ireland | 1,200 | 1,700 | 1 | 6 |
| Netherlands | 3,900 | 2,300 | 0 | 3 |
| Germany | 21,000 | 2,100 | 0 | 2 |

## Step 2: Normalise each column to 0–100
Normalised = (value − column min) ÷ (column max − column min) × 100

Example, UK firms: (9,800 − 1,200) ÷ (21,000 − 1,200) × 100 = **43.4**

| Market | Firms | Spend | Language | Partners |
|---|---|---|---|---|
| UK | 43.4 | 33.3 | 100 | 100 |
| Ireland | 0.0 | 0.0 | 100 | 66.7 |
| Netherlands | 13.6 | 100 | 0 | 16.7 |
| Germany | 100 | 66.7 | 0 | 0 |

## Step 3: Weight and sum
**Weights:**
- Firms 35%: the size of the prize
- Spend 25%: willingness to pay
- Language 25%: we only have English today
- Partners 15%: our distribution

UK = 0.35 × 43.4 + 0.25 × 33.3 + 0.25 × 100 + 0.15 × 100 = **63.5**

| Market | Score | Rank |
|---|---|---|
| UK | 63.5 | 1 |
| Germany | 51.7 | 2 |
| Ireland | 35.0 | 3 |
| Netherlands | 32.3 | 4 |

## Step 4: Sanity check and verdict
- **Deepen the UK first.** It's the only market strong on both language and partners.
- **Germany is the biggest prize.** It scores 0 on language and partners, so it needs a German-language product and a channel partner before entry.
- **Change a weight by 10 points and re-rank.** If the order flips, the decision is close: say so.
