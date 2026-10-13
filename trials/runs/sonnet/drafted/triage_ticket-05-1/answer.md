Every ticket result now carries a `fallbacks` list showing which fields the model gave no usable answer for.

- **Real verdict:** `fallbacks` is `[]`. A genuine "general / normal" from the model is empty here.
- **No real verdict:** `fallbacks` names the fields that were defaulted, e.g. `["queue", "urgency", "summary"]` for your "Help!!" ticket.
- **Partial verdict:** if only the urgency was unusable, you'd see `["urgency"]`, so you know the queue was still judged.
- **Enterprise:** a defaulted `normal` that gets raised to `high` is still flagged.

Your ticket list can show or sort on a non-empty `fallbacks`, so those tickets get opened straight away.

## What changed
- `seam.py`: records which fields fell back, then applies the same defaults as before. Queue, urgency, deadline, summary and tier handling are unchanged, and there is no extra model call.
- `test.py`: existing expectations updated, and three tests added covering a genuine general/normal, per-field flags, and the enterprise case. All 14 tests pass, and nothing paid was run.
- `README.md`: documents the new field.

## For you to decide
- **Charter:** `evals/triage_ticket/charter.md` lists the output as four fields, so it is now slightly out of date. I haven't touched it, since only you change a charter. The new field adds no decision for the model and moves no line.
- **List display:** I couldn't see your ticket list code, so wiring `fallbacks` into the display (a badge, a sort, a separate view) still needs doing wherever that lives.
- **Possible follow-up:** this flags tickets where the model's answer was unusable. It does not catch a model that confidently answers "general / normal" for a ticket like the label one. That would be a question about the model's judgement, which the charter leaves to it, and I'd want your decision before changing it.