# Kano: the full method

## The two questions (per feature)
- **Functional:** "If [product] had [feature], how would you feel?"
- **Dysfunctional:** "If [product] did NOT have [feature], how would you feel?"

Answers: 1 I like it · 2 I expect it · 3 I'm neutral · 4 I can live with it · 5 I dislike it

## Evaluation table (rows = functional, columns = dysfunctional)
| F \ D | Like | Expect | Neutral | Live with | Dislike |
|---|---|---|---|---|---|
| **Like** | Q | A | A | A | **O** |
| **Expect** | R | I | I | I | **M** |
| **Neutral** | R | I | I | I | **M** |
| **Live with** | R | I | I | I | **M** |
| **Dislike** | R | R | R | R | Q |

## Categories and what to do
| Code | Category | Meaning | Goal | Benchmark |
|---|---|---|---|---|
| **M** | Must-be | Expected. Absence angers; presence earns nothing extra | **Parity**: match the market reliably. Don't gold-plate | Track NPS and complaints when it breaks |
| **O** | One-dimensional (performance) | More is better, linearly | Compete here: aim to beat named competitors | Benchmark against competitors on this metric |
| **A** | Attractive (delighter) | Delights when present, not missed when absent | Include selectively; it needn't be best-in-class | Re-survey: delighters **decay** into performance, then must-be |
| **I** | Indifferent | No effect either way | Don't build. Keep surveying for category shift | — |
| **R** | Reverse | Some people actively don't want it | Make it optional, or don't build it | Check which segment says this |
| **Q** | Questionable | Contradictory answers | Exclude. If over about 10%, the question was unclear | — |

## Coefficients (per feature)
- Better = (A + O) / (A + O + M + I): how much satisfaction rises if you add it (0 to 1)
- Worse = −(O + M) / (A + O + M + I): how much it falls if you leave it out (0 to −1)

Plot Better (y) against |Worse| (x). Top right = performance, bottom right = must-be, top left = delighter.

## Worked example (SYNTHETIC: Fernhill Coffee, 20 respondents, feature "pause my subscription")
- Answers: 12 × (Expect, Dislike) = M; 5 × (Like, Dislike) = O; 3 × (Neutral, Neutral) = I
- `kano_summary()` gives category **M** (60%), Better 0.25, Worse −0.85
- Decision: build pause to parity with competitors, don't market it, and watch cancellations if it breaks.
