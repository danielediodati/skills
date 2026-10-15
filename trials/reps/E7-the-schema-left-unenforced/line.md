# E7 - the line a replay is judged on

Seams: planner (`src/trainer/coach/planner.py`); logger (`src/trainer/coach/logger.py`)

Where the design puts it: ADR-0004 item 3. Both seams emit through the provider code in `src/trainer/coach/`.

## Constrained
- An emitted `exercise_id` is one of today's admissible ids, held at decoding: the emit schema is built per request with the id as an enum of today's admissible set, and the provider is asked to enforce it, so constrained decoding cannot produce an invented id. A provider path that sends the schema without asking for it to be enforced leaves the id to the model, with only the validator's refusal after the fact.
