Each result from `triage_ticket` now carries an `unjudged` list, so tickets that arrived without a real verdict can be told apart from genuine general/normal ones. All 14 tests pass.

**What changed**
- **`seam.py`:** the result gains `unjudged`, a list naming which of `queue`, `urgency` and `summary` came from a code fallback because the model's answer was missing or outside the allowed lists.
- **Genuine verdicts:** a ticket the model really judged as `general` / `normal` has `unjudged == []`.
- **Your "Help!!" case:** if the model's answer was unusable, the ticket still shows as general / normal / "Help!!", but with `unjudged == ["queue", "urgency", "summary"]`.
- **Enterprise customers:** the one-level raise doesn't hide an unjudged urgency. A `normal` fallback that becomes `high` is still flagged.
- **`test.py`, `README.md`:** tests cover the flag, and the README documents the new field.

**What I left alone**
The fallback values (`general`, `normal`, subject as summary) and the model's prompt are unchanged. Whether a ticket with a failed verdict should still default to `general`/`normal` is your decision, not something I changed.

**Needs your side**
- **Ticket list:** this code only produces the flag. The list UI that agents use has to show `unjudged` (a badge, a sort, or a filter on non-empty) for anyone to see it. That code isn't in this directory.
- **Tickets with real verdicts:** a ticket the model read and wrongly called general/normal has an empty `unjudged`. This flag catches tickets with no verdict, not wrong verdicts.