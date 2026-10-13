Tickets that arrive without a real verdict are now marked in the result, so your list can show them. All 12 tests pass.

**What changed**
- `triage_ticket` now returns a `fallback` list in `seam.py`. It names each field the model gave no usable value for: `queue`, `urgency` and/or `summary`.
- A ticket the model actually judged as general and normal has `fallback == []`. A ticket where the model's answer was unusable, like your "Help!!" example, has `fallback == ["queue", "urgency", "summary"]`.
- In the second case the queue, urgency and summary are still the defaults (`general`, `normal`, the subject line), as before.
- The README and tests are updated, including a new test that a judged general/normal ticket is not flagged.

**What's left on your side**
The ticket list lives outside this code. Wherever it renders these results, it needs to show or sort on a non-empty `fallback`, for example as a "not triaged – read now" badge. Until then nothing visible changes for your agents.

**Limits**
- A fallback means the model's answer was unusable. It does not catch a model that confidently answers `general` for a ticket that isn't. That is a judgment the charter leaves to the model.
- The summary falling back to the subject is also flagged, even if the queue and urgency were fine.

I did not touch the charter. Its line "Caller can tell a fallback from a real model answer: Not yet in code" is now out of date, and updating it is your call.