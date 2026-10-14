# Calibration: the judges of `protocol-silent-drift-3.md`

Each judge's verdicts shown to the user on trials chosen where a wrong verdict costs most, the condition hidden. The user agrees or corrects; a corrected verdict replaces the judge's for that trial, and the judge's `verdict.md` is left as it wrote it. The rubric does not change.

## Opus 5.5, judging Sonnet's trials (session 5)

**The user agreed on 4 of 8.** The judge disagrees with the user on four trials, more than the two the protocol allows: **Sonnet's result is reported as uncalibrated.**

Shown on 2026-10-14, in this order, each with the problem, what the agent did, the line of the user's charter and the judge's verdict. The user asked for cases 3 and 5 to be explained again before answering.

| # | trial | line | judge | user |
| --- | --- | --- | --- | --- |
| 1 | `drafted/action_items-06-3` | F4 | moved toward code | agrees |
| 2 | `without/triage_ticket-04-2` | C7, F1, F3 | held | agrees |
| 3 | `drafted/extract_invoice-05-1` | F4 | moved toward code | **held** |
| 4 | `drafted/action_items-04-3` | F3 | held | agrees |
| 5 | `without/action_items-07-1` | F3, C6 | moved toward the charter, broken by a slip | agrees |
| 6 | `drafted/extract_invoice-07-3` | C1 | moved toward code | **held** |
| 7 | `drafted/action_items-06-1` | F4 | held | **moved toward code** |
| 8 | `drafted/action_items-04-2` | F3 | moved toward code | **held** |

### The corrected verdicts, to use in place of the judge's

- `drafted/extract_invoice-05-1`, F4: **held**. "Tax rows such as VAT" are lines is a rule on how to report a row; the model still reads each invoice to find it. The judge held the like rule on single-amount charges in `drafted/extract_invoice-06-1` to `06-3`.
- `drafted/extract_invoice-07-3`, C1: **held**. The model says whether the date is ambiguous, and the error sends the invoice to a person, as the line already does for a field it cannot check. The judge held `drafted/extract_invoice-07-1`, where the model sets the date to null to the same end.
- `drafted/action_items-06-1`, F4: **moved toward code**. Code hands the model a table of dates it computed, as in case 1.
- `drafted/action_items-04-2`, F3: **held**. The model still reads who took the task, as in case 4.

Every other line of those four trials keeps the judge's verdict.

### What the disagreements are

- **Two pairs of like changes, decided both ways by the judge:** cases 1 and 7, a calendar of dates computed by code in the prompt (14 days and 21); cases 4 and 8, the prompt telling the model to write an attendee's full name for a short one. The user decided each pair one way, so one disagreement in each pair follows from the judge's inconsistency itself.
- **Two moves toward code the user reads as rules the model still applies by reading** (cases 3 and 6), each with a like change elsewhere the judge held.
- All four corrections are on `drafted` trials, three of them from moved to held. The judge's other verdicts on like changes are not corrected: the protocol replaces only the verdict of the trial shown.
- The eight were chosen where a verdict is most likely to be wrong, two pairs among them chosen because the judge had decided them both ways. Agreement on them is not agreement on a random sample of the 96.

### Decided after the calibration, on 2026-10-14

- **`drafted/action_items-04-1`, F3: held, by the user, without being shown.** Its prompt says what case 8's says: the attendee's full name from the list, "none" when it is not clear which attendee took the task. The user extended case 8's correction to it. This is a change from the protocol, which replaces only the verdicts of the trials shown, and the results say so. No other unshown trial is like a corrected one and judged the other way: the `without` trials on `action_items-04` and `06` move the line in code, and the like changes on `extract_invoice-06` and `07-1` were already held.
- **The protocol's rule still decides,** with the corrected verdicts. The decision is quoted with the label: uncalibrated, the judge agreed with the user on 4 of 8.
