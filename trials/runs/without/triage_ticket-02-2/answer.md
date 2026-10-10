`triage_ticket` now returns a `fallbacks` list naming each of queue, urgency and summary that is a stand-in rather than the model's own answer. The 14 tests pass.

**What changed**
- **New field:** `fallbacks` is a list drawn from `"queue"`, `"urgency"` and `"summary"`. It is empty when the model answered all three.
- **When a field is listed:**
  - `queue` or `urgency` is listed when the model's answer was missing or not in the allowed list.
  - `summary` is listed when it was missing or empty and the subject was used instead.
- **Your two examples:**
  - "Parcel arrived smashed" came back with no usable answer, so it now carries `["queue", "urgency", "summary"]`.
  - The opening-hours ticket, where the model genuinely said general/normal, carries `[]`.
- **Enterprise raise:** `urgency` stays listed when a stand-in `normal` was raised to `high` for an enterprise customer, because the value is still not the model's judgement.
- **Files touched:** the changes are in `seam.py`, `test.py` and `README.md`.

The UI rule is then simply: show "check me" when `fallbacks` is non-empty, and optionally say which field.

**Things to know**
- `fallbacks` is an added key, so existing callers keep working. Only code that compares the whole result dict for equality would notice, as the existing tests did, and I updated those.
- A summary the model wrote that happens to equal the subject is not flagged, because it did answer.
- A summary cut to 120 characters is not flagged either, since it is still the model's own text.
- A ticket where only the summary fell back (the model gave a valid queue and urgency) is flagged on `summary` alone. Decide whether that deserves the same "check me" as a wrong queue, or something lighter.