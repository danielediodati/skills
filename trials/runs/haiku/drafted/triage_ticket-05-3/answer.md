Tickets that fell back to the defaults are now marked `judged: False`, so they can be told apart from real general/normal verdicts. The change is in `seam.py`, and the tests pass (14/14).

**What changed**
- `triage_ticket` returns a new `judged` field. It is `True` only when the model's answer gave a valid queue and a valid urgency. It is `False` when either one was missing or invalid and fell back to `general` or `normal`.
- Fallback values, the closed lists, the SLA table and the enterprise rule are unchanged. The field only reports what already happened.
- `test.py` has three new tests covering judged and not-judged cases. The two existing tests that compare the full result now include `judged`.
- `README.md` documents the new field.

**What it does not catch**
The flag only detects a missing or invalid answer. If the model read "Help!!" with a description of a station outage and still answered `general` / `normal`, the ticket is marked `judged: True`, because that is a real verdict, just a wrong one. Catching that would mean a code heuristic on the judgement, which the charter leaves to the model. The model's queue and urgency choice is one of the free decisions.

**Things for you to handle**
- **Charter:** `evals/triage_ticket/charter.md` still lists the output as four fields. I did not edit it, since only you change charters. Its Output line should add `judged`.
- **Ticket list:** the list view is outside this repo. It needs to show `judged` and sort or filter on it, so that `judged: False` tickets get a person straight away.
- **Last Tuesday's ticket:** I can't tell from the code whether it would have been flagged. That depends on whether the model's raw answer was unusable. This code doesn't log raw answers, so the stored output for that ticket, if you have it, would settle it.

No paid calls were made.