Tickets now carry a "was this really judged" flag, so the ticket list can tell a genuine general/normal verdict from a fallback. All 14 tests pass.

**Cause:** the code replaced anything it couldn't use from the model's answer with `general`, `normal` and the subject line. A real verdict and a fallback therefore came out looking identical.

**Change (in `seam.py`):** `triage_ticket` now returns two extra fields:
- `needs_review`: `True` if any part of the answer was a fallback.
- `defaulted`: which fields were filled in by fallback, from `queue`, `urgency` and `summary`. For example, `["queue", "urgency", "summary"]` when the model's answer was unusable.

**Behaviour:**
- **Real general verdict:** a ticket where the model really said `general` / `normal` with its own summary gets `needs_review: False`, so it stays low-key.
- **Last Tuesday's ticket:** a "Help!!" ticket with an unusable model answer comes out `general` / `normal` / "Help!!" with `needs_review: True`.
- **Enterprise tier:** the one-level urgency raise does not clear the flag.

**What you need to do:** show `needs_review` in the agents' ticket list, for example as a marker or a separate "unsorted" view. I only changed the function's output, not the list itself, since that code isn't in this folder.

**Tests and docs:** I updated the two existing exact-match tests to include the new fields and added tests for the real-verdict case, each single fallback, and the enterprise case. `README.md` documents the new fields.

The flag only covers answers the code couldn't use. If the model confidently answers `general` / `normal` for a ticket that isn't, that case isn't flagged.