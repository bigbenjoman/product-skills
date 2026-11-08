---
name: usability-test
description: "Plan, run and synthesise usability tests on a prototype or live product: choose lab (moderated, observation room), remote moderated, unmoderated (UserTesting, Maze, Lyssna) or guerrilla street/café intercepts; write the task script, run think-aloud sessions, code findings by severity, score SEQ/SUS, fix and re-test (5 users x 3 rounds). Covers consent, incentives and AI-assisted synthesis. Use when the user asks to user test, usability test, test a prototype, guerrilla test, hallway test, get feedback on a design, or check whether people can use something before building or launching it."
metadata:
  version: 0.1.0
---

# Usability Test

Until an idea is in a customer's hands, you don't know. Usability testing answers **"can they?"**. It does not answer "will they pay?" (use `demand-test` for that) and it does not answer "which is better at scale?" (use `experiment-design` for that).

## Step 1: Choose the format
| Format | When | Cost and time | Watch out |
|---|---|---|---|
| **Lab** (moderated, observation room) | High-stakes flows, many stakeholders who need to watch, new markets | £££, 1–2 weeks | Slow; artificial setting |
| **Remote moderated** (video call, screen share) | Most B2B; specific recruits | ££, a few days | Hard on TV or mobile hardware |
| **Unmoderated** (UserTesting, Maze, Lyssna) | Quick checks on clear tasks; overnight results | £–££, 24–48h | No follow-up questions; professional testers |
| **Guerrilla intercept** (street, café, station, shop floor) | Consumer products; early prototypes; "can a stranger do this in 2 minutes?" | £, same day | Not your exact customer; short sessions only |

Practice: at LOVEFiLM, Ben stopped people in the street with a prototype. At Studia the team does the same today. At DAZN, launch markets were tested in a lab with an observation room.

## Step 2: Write the task script (`references/session-guide.md`)
- 3–5 tasks, each a **goal**, not an instruction. "You don't want reminders going out at weekends" is a goal. "Click Schedule" is an instruction.
- Set the success criterion for each task **before** the session.
- Make the stimulus match the market: local currency, local content, local imagery.

## Step 3: Run 5 users per round, think-aloud
1. Consent and recording permission; explain "we're testing the product, not you".
2. Ask them to think aloud. Don't help. If they ask a question, answer with "what would you do if I weren't here?"
3. After each task, ask the **SEQ**: "How easy was that?" (1 = very hard, 7 = very easy).
4. At the end, 2 minutes on "what was most confusing?" and an optional **SUS** (10 items) for a benchmark.
5. Note-taker logs: task, success / partial / fail, time, quote, observed problem.

## Step 4: Code and fix
Severity:
- **S1** blocks the task
- **S2** causes a detour or error
- **S3** cosmetic or a hesitation

Count how many of the 5 users hit each issue. Fix every S1 and S2, then run **round 2 with 5 new people**. Usually 3 rounds per segment.

## Step 5: Synthesise (AI-assisted)
Transcribe the sessions. Use the `customer-evidence` skill to code the transcripts, with the severity rubric. **A human watches at least 2 sessions per round.** Agents miss tone, hesitation and where people looked.

## Ethics and incentives
- Written or recorded consent.
- No recording of anyone under 18 without a guardian's consent.
- Store recordings securely and delete them after synthesis (GDPR).
- Incentives: a coffee or a £10 voucher for 5-minute guerrilla sessions; market rate for 30–60-minute sessions.

## Output
- `references/findings-template.md`: tasks × users grid, issues ranked by severity × frequency, fixes, and round-over-round comparison.
- Worked example: `references/worked-example.md`.
