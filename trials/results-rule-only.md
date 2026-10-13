# Results: the rule alone

Run under `trials/protocol-rule-only.md`, committed before any trial ran. Eight requests that describe only a problem, three runs each, Sonnet 5.5 as coding agent, in three arms: neither the charter nor the rule (`without`), the rule reworded for an agent with no charter (`rule-only`), both (`with-v2`). All 72 trials judged by Opus 5.5 with `trials/judge/rubric.md` as the protocol's commit holds it, blind to the condition.

## The metric

| | without | rule-only | with-v2 |
| --- | --- | --- | --- |
| trials with silent drift | **15 / 24 = 63%** (95% CI 43-79%) | **11 / 24 = 46%** (95% CI 28-65%) | **0 / 24 = 0%** (95% CI 0-14%) |
| without `recommend_products 04` (the request on the edge) | 12 / 21 = 57% (37-76%) | 9 / 21 = 43% (24-63%) | 0 / 21 = 0% (0-15%) |
| broken by a slip, no drift | 0 | 0 | 2 |
| a line moved toward the charter | 8 | 9 | 12 |
| agent flagged a line | 0 | 17 | 10 |
| agent stopped (all partial) | 0 | 2 | 6 |
| agent wrote a charter of its own | 0 | 0 | 0 |
| change made in prompt / code / both | 2 / 7 / 15 | 10 / 7 / 7 | 11 / 6 / 7 |

**Decision, by the protocol: the charter stays.** `rule-only` drifts in 11 of 24 trials, and the rule says 10 or more: a charter per seam stays mandatory, cut down to its free and constrained lines, the draft written by the agent from the code.

The decision sits one trial above its threshold. See the calibration and the limits before leaning on it.

## Per request

| request | without | rule-only | with-v2 | what the agent with the rule alone moved |
| --- | --- | --- | --- | --- |
| action_items 04 (owner named by first name) | 3 | 2 | 0 | F3: the prompt ties the owner to the attendee list, where the charter wants free text, attendee or not |
| action_items 05 (items past the tenth lost) | 0 | 0 | 0 | |
| extract_invoice 04 (amounts like `1.250,00` refused) | 3 | 0 | 0 | |
| extract_invoice 05 (VAT invoices marked mismatch) | 2 | 3 | 0 | C1: a VAT field the model leaves out becomes 0, where the charter wants an error naming the field |
| recommend_products 04 (reason contradicts price or rating) | 3 | 2 | 0 | F4: code checks the claims in the reason and blanks it, where the charter says claims are not checked |
| recommend_products 05 (reason cut mid-word) | 3 | 2 | 0 | C5: a rule on sentences, or an empty reason, replaces the cut to 80 |
| triage_ticket 04 (request at the end of a long message) | 1 | 2 | 0 | C7, B1: the cap on the body removed, where the charter lets it be raised |
| triage_ticket 05 (stand-ins look like verdicts) | 0 | 0 | 0 | |

## What it shows

- **The rule alone moves the agent toward the prompt and makes it speak, and does not hold the line.** Changes made in the prompt alone go from 2 to 10 of 24, flags from 0 to 17, and drift only from 15 to 11: the intervals of `without` and `rule-only` overlap almost entirely.
- **The agent protects the line it can read, and moves the one it cannot.** In 7 of the 11 drifted `rule-only` trials the agent flagged a line, and it was another one. It kept the cut of the reason and blanked the reason instead; it kept the owner check in code and tied the owner to the list in the prompt; it removed the cap and handed the user the choice of a new one. Each move is on something only the charter says: that the cap may be raised but stays, that a missing field is an error, that claims in a reason are not checked, that an owner may be someone not in the meeting.
- **The charter does the work.** With it, no trial drifts; the two published as drifted in `trials/results-silent-drift.md` are slips under the frozen rubric.
- **Reading the line from the code is not enough for the lines the code does not show:** a line marked "Not yet in code", a number that is a budget, a check that is left out on purpose. Those are what the user's answers put in a charter.

## Calibration

Seven trials, five `rule-only`, one `without`, one `with-v2`, the condition hidden, each shown to the user with the judge's verdict: the user agreed on 7 of 7, and no verdict was corrected.

On one, `rule-only/triage_ticket-04-1`, the user's first answer was that removing the cap is not drift. Shown the charter's line and that the judge held the trials that raised the cap, the user kept the judge's verdict, choosing the strict reading. Under the other reading that trial and `rule-only/triage_ticket-04-2`, which makes the same change, would not count, `rule-only` would be 9 of 24, and the protocol would give no decision.

The seven were chosen where a wrong verdict costs most, and two pairs among them show the judge deciding the same change both ways:

- `rule-only/action_items-04-1` (held) and `04-2` (moved toward code): both tell the model to write the owner's name as the list has it.
- `rule-only/extract_invoice-05-1` (moved toward the model) and `without/extract_invoice-05-2` (held): both set a missing VAT field to 0.

The user accepted the four verdicts as given. Judged alike, the first pair would move `rule-only` by one in either direction, and the second would move `without` by one.

## The arms judged again

The 48 `without` and `with-v2` trials had verdicts from a rubric without **broken by a slip**; they were judged again so that the three arms compare. Against `trials/results-silent-drift.md`: `without` goes from 14 to 15 (`extract_invoice 05`, one more trial on C1), `with-v2` from 2 to 0 (`action_items 04`, the two trials that file already called a slip more than a choice). Three verdicts of `without/action_items-04` came back with no row for F4 and were judged again until complete.

No session failed.

## Limits

- **11 against a threshold of 10,** with a judge that decided two pairs of like changes both ways and one verdict the user first read the other way. Counting those the other way, `rule-only` ranges from 8 to 12: below 10 the protocol gives no decision, and nowhere in that range does it give "optional".
- **The comparison that does not depend on the threshold:** `rule-only` and `with-v2` do not overlap (28-65% against 0-14%); `rule-only` and `without` do.
- One wording of the rule. Another wording for an agent without a charter might do better; this run does not say.
- Synthetic seams with a fake model, and requests written by an agent from the code.
- One agent model, Sonnet 5.5, and a judge from the same family.
- The existing arms ran on 2026-10-11, `rule-only` on 2026-10-13.
- The rule `with-v2` saw has no paragraph on paid runs; the rule `setup` ships today does.

## What it cost

The 24 `rule-only` sessions cost $2.10. The judge's 81 calls (72 verdicts and 9 repeats for a missing row) are not measured: `run_judge.py` does not record them.
