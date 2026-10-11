`triage_ticket` now reports which fields were filled in with a default because the model gave no usable answer. A genuine `general` / `normal` verdict can be told apart from one that never got judged. All 15 tests pass.

**Cause**
When the model's answer was missing or unparseable, `seam.py` silently substituted `general`, `normal` and the subject line as the summary. The result was identical to a real verdict, which is why last Tuesday's "Help!!" ticket looked like any other low-stakes ticket.

**Change**
- **New key:** the returned dict gains `fallbacks`, a list of any of `"queue"`, `"urgency"`, `"summary"` that were defaulted.
- **Genuine verdicts:** `fallbacks == []` means the model really answered. A real `general` / `normal` with a short subject has an empty list.
- **Undecided tickets:** "Help!!" with an unusable answer gives `fallbacks: ["queue", "urgency", "summary"]`.
- **Enterprise customers:** the one-level urgency raise no longer hides an unjudged urgency. A defaulted urgency is still flagged after the raise.
- **Existing keys:** `queue`, `urgency`, `summary` and `respond_within_hours` are unchanged, so nothing downstream breaks.

I also updated `README.md` and added tests for genuine versus defaulted verdicts, a missing summary, and the enterprise case.

**Still to do**
The ticket list itself isn't in this repo, so it still has to show `fallbacks`. I'd show a "not triaged" badge whenever it's non-empty and sort those tickets to the top.

**Still open**
These tickets still get `normal` / 24h as their deadline. If you'd prefer them to get a shorter deadline until a person has looked, that's a one-line change, but it's your call as it changes the response promise.