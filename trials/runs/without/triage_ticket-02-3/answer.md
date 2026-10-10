Results now say when a field is a stand-in, and which one. All 14 tests pass.

**What changed**

- `seam.py`: `triage_ticket` returns an extra key, `fallbacks`, a list naming which of `queue`, `urgency` and `summary` are stand-ins rather than the model's own answer.
- Empty list: the whole result is the model's judgement.
- "Parcel arrived smashed" with an unusable answer now returns `fallbacks: ["queue", "urgency", "summary"]`, so it gets the "check me" marker.
- The opening-hours ticket, where the model really answered `general` / `normal`, returns `[]`.
- `queue` is flagged when the model's value is missing or not one of the five queues.
- `urgency` is flagged when the model's value is missing or not one of the four levels.
- `summary` is flagged when it is missing or blank and the subject line was used instead.
- `README.md` documents the new key.
- `test.py` has new cases for the above, and the existing exact-dict assertions include `fallbacks`.

**Decisions to confirm**

- **Enterprise bump:** if the urgency was a stand-in (`normal`) and the enterprise rule raised it to `high`, it is still flagged as a fallback. The `high` comes from a guess, so it needs a check.
- **Existing fields:** `queue`, `urgency`, `summary` and `respond_within_hours` are unchanged, so current consumers keep working. The one exception is code that compares the whole result dict for equality, which will now see the extra key.

You can show the marker with `if result["fallbacks"]:`, and the list tells the team lead which part to re-check.