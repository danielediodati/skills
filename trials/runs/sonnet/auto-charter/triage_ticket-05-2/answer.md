`triage_ticket` now returns a `defaulted` list with every result, so a real verdict can be told apart from a fallback. All 14 tests pass, but I haven't touched your ticket list, so that still needs wiring.

**What it does**
- `defaulted` names the fields (`queue`, `urgency`, `summary`) that the model didn't usefully answer, meaning the answer was missing, unparsable or off-list.
- A model that really says `general` / `normal` with a real summary gets `defaulted == []`.
- A ticket like "Help!!" that came back unusable gets `["queue", "urgency", "summary"]`, even though it shows as General, normal, 24 hours.
- Enterprise uplift is applied after this check, so an uplifted default is still reported as defaulted.

**What didn't change**
- Routing, fallback values, deadlines, the enterprise uplift and the single model call are all as before.
- The charter is untouched. The fallback is still `general` / `normal`; the result just says when it was used.

**What you need to do**
- In the ticket list, flag or sort tickets where `defaulted` is non-empty. That list lives outside this repo, so I couldn't wire it.
- A defaulted ticket tells you the model produced no usable verdict, not that the ticket is important. Many will be ordinary, but a person should open them first.

Changes are in `seam.py`, with new tests in `test.py` and the field documented in `README.md`.