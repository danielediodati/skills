The result now says which of queue, urgency and summary were stand-ins. I couldn't run the tests, because the shell command was denied, so please run `python -m unittest` yourself.

**What changed**
- **`seam.py`**: a queue or urgency the model didn't give validly is now `None` instead of `general` / `normal`.
- **`respond_within_hours`**: it is `None` when the urgency is `None`.
- **Enterprise raise**: the raise only applies when there is an urgency to raise.
- **`stand_ins`**: a new field listing which of `queue`, `urgency` and `summary` were not the model's judgement. For "Parcel arrived smashed" with an unusable answer you'd get `queue: None`, `urgency: None`, `summary: <subject>`, `stand_ins: ["queue", "urgency", "summary"]`.
- **`test.py` and `README.md`**: updated to match, with new cases for each single stand-in field and for enterprise with an unknown urgency.

**Why `None` and not a flag on top of the defaults**
`evals/triage_ticket/charter.md` already says an invalid field is `null`, never a default, and notes that the code didn't do this yet. So this brings the code in line with the charter, and I didn't change the charter.

**What this means for you**
- Tickets the triage gave up on will no longer sit in `general` / `normal`. The queue and urgency will be `None`, so whatever renders the list has to handle that. `stand_ins` is the thing to key the "check me" marker on.
- A real `general` is now a ticket the model actually chose `general` for.
- The summary fallback to the subject is unchanged (the charter allows it), but it is now flagged.