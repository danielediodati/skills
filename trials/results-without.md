# Results without the charter

Judged by Opus 5.5 with `trials/judge/rubric.md`. The judge was calibrated after ticket 06 on seven trials drawn from both conditions; the user agreed with all seven, and these verdicts stand. The comparison with the charter is in `trials/results.md`.

36 trials: twelve requests, three times each, Sonnet 5.5 as coding agent, no charter and no rule.

**27 of 36 trials drifted** (at least one line moved toward code or toward the model). The gate is 12: the session goes on to ticket 06.

No agent flagged a line, and none stopped.

| request | drifted | lines moved (in all three runs unless noted) | where |
| --- | --- | --- | --- |
| action_items 01 | 3/3 | F3 owner, toward code | code, both |
| action_items 02 | 3/3 | F4 deadline, toward code | both, prompt |
| action_items 03 | 0/3 | F3 owner, toward the charter | both |
| extract_invoice 01 | 3/3 | F6 non-integer quantities, toward code | code |
| extract_invoice 02 | 3/3 | C1 answer shape, toward the model; C3 net/VAT/total, toward the charter | both |
| extract_invoice 03 | 3/3 | C1 answer shape, toward the model | code |
| recommend_products 01 | 3/3 | F1 which products, C1 full catalogue to the model, toward code; C2 in one run | code |
| recommend_products 02 | 3/3 | F3 how many, C4 empty strip without fallback, toward code | code |
| recommend_products 03 | 3/3 | F4 what the reason says, toward code | code |
| triage_ticket 01 | 3/3 | F1 queue, F2 urgency, F3 summary, C7 what the model sees, toward code; C8 in one run | code, both |
| triage_ticket 02 | 0/3 | C3 `null` for an invalid field, toward the charter | code |
| triage_ticket 03 | 0/3 | none | code |

Each trial's diff, answer and verdict are in `trials/runs/sonnet/without/<seam>-<request>-<run>/`.
