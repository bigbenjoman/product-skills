---
name: demand-test
description: "Test whether customers WANT something before building it: fake door / painted door buttons, smoke-test landing pages with ads, pre-sales and letters of intent, concierge MVPs and Wizard-of-Oz prototypes. Sets the success threshold before the test, sizes the sample, reads results with a Wilson confidence interval, and handles ethics and UK law (honest disclosure, no card capture, PECR/GDPR consent, CMA guidance). Use when the user asks for a fake door test, painted door, smoke test, landing-page test, waitlist, pre-sell, concierge or Wizard of Oz MVP, or 'will anyone actually want this'."
metadata:
  version: 0.1.0
---

# Demand Test

Usability tests ask "can they?". Demand tests ask **"will they?"**. They use behaviour, not opinion.

## Step 1: Pick the method
| Method | What it is | Best for | Evidence strength |
|---|---|---|---|
| **Fake / painted door** | A real-looking button or option for a feature that doesn't exist yet. The click opens an honest "coming soon" message | A new feature inside an existing product | Medium: a click is cheap |
| **Smoke test** | A landing page plus a small ad spend. Measure sign-ups to a waitlist | A new product or proposition | Medium |
| **Pre-sell / LOI** | Take a deposit, or get a signed letter of intent | B2B, or high-priced consumer products | High: money or a signature |
| **Concierge** | Deliver the service by hand to the first customers, and they know it | Services; complex B2B | High, but small n |
| **Wizard of Oz** | Customers think it's automated; humans do it behind the scenes | Testing the experience before building automation | High on experience; not on cost |

## Step 2: Write the decision rule FIRST
"If **≥ X%** of **[eligible people]** do **[action]** within **[days]**, we build it. If **< Y%**, we drop it. In between, we iterate the offer."

Set X from the business case: what rate makes the feature pay?

## Step 3: Size it
Use `pricing_toolkit.n_for_margin(p, margin)`. Example: expected rate 15%, ±3 points → **545** eligible people.

## Step 4: Run it honestly (the ethics and law are part of the method)
- **The door must tell the truth on click.** Example: "Annual billing is coming soon. We've noted your interest. Nothing has been charged." Never capture card details for something that doesn't exist.
- **Waitlist emails:**
  - separate, unticked consent for marketing (PECR/GDPR)
  - say what you'll send and how often
  - easy to unsubscribe
- **Smoke-test pages** must not claim the product exists or make price promises you won't keep (CMA guidance on misleading actions).
- Remove the door when the feature ships or the test ends. Then tell the people who clicked.

## Step 5: Read it with a confidence interval
Use `pricing_toolkit.wilson(successes, n)`. Decide on the interval, not the point estimate:

- the whole interval is above X → **build**
- the whole interval is below Y → **drop**
- it straddles a threshold → extend the test or iterate the offer

## Worked example
See `references/worked-example.md`.
