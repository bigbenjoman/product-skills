# Codebook example (SYNTHETIC: Oakbill Chase, an AI add-on that chases late invoices, 300 support tickets and reviews)

| Code | Theme | Definition | Include if… | Example verbatim | Count | Severity |
|---|---|---|---|---|---|---|
| C01 | Wrong invoice details | The reminder quoted the wrong client, amount or due date | Owner or client reports a factual error | "It said £1,200, the invoice was £2,100" | 41 | 3 |
| C02 | Client annoyed by the chaser | The client objected to an automated reminder | Mentions a client complaining or asking for a person | "Two clients replied asking why a robot was chasing them" | 33 | 2 |
| C03 | Too slow to tell me | The summary text arrived late | Delay is mentioned | "Got the text 20 mins later, I'd already rung the client" | 27 | 2 |
| C04 | Setup confusing | Trouble connecting the bank feed or invoice ledger | During the first week | "Couldn't work out the bank feed" | 22 | 2 |
| C05 | Price worry | Concern about cost relative to value | Mentions price or value | "£40 a month is a lot in a quiet quarter" | 15 | 1 |

**Rules:**
- One ticket can carry several codes.
- Spot-check 10% by hand. Under 90% agreement means you rewrite the definitions.
- Rank by count × severity: C01 (123) > C02 (66) > C03 (54) > C04 (44) > C05 (15).
