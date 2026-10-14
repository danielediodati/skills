Tickets that the model didn't actually answer now carry `judged: False`, so the list can flag them. All 14 tests pass with `python -m unittest`.

**What changed in `seam.py`**
- `triage_ticket` returns a new key, `judged`. It is `True` only when the model's answer gave a usable queue, a usable urgency and a summary.
- If any of those three is missing or invalid, `judged` is `False`. The fallbacks (`general`, `normal`, the subject line) still apply, so routing is unchanged.
- An enterprise bump doesn't affect `judged`.

**Tests and docs**
- Updated the two full-dict assertions that now include `judged`.
- Added tests for a fully judged `general`/`normal` ticket, a partial answer (valid queue, invalid urgency), and an answer with no summary.
- Documented `judged` in `README.md`.

**What you still need to do**
- The ticket list isn't in this directory, so I couldn't wire it up. Your list needs to read `judged` and show `False` tickets prominently, for example with a badge or a sort to the top. The "Help!!" ticket would have come back `judged: False`, because the model's answer had no usable summary.
- `judged: True` means the model answered, not that its answer is right. A warehouse outage could still come back as `general`/`normal` with a valid-looking summary. The flag only separates "read" from "not read".

I didn't change how unjudged tickets are routed, since you asked for them to be visible, not re-prioritised. If you want them to be treated as `high` until someone reviews them, that's a small follow-up.