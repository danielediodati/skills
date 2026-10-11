The result now says when a field is a stand-in, and which one. All 12 tests pass.

**What changed in `seam.py`**
- A queue or urgency the model didn't give validly is now `None`, no longer `general`/`normal`. That is what the charter already specified; the code just hadn't caught up.
- `respond_within_hours` is `None` when the urgency is `None`. The enterprise raise is skipped in that case.
- A missing summary still falls back to the subject, which the charter allows.
- There is a new `stand_ins` list in the result, for example `["queue", "urgency", "summary"]`. It names each field that isn't the model's own judgement, and is empty when all three are.

Your "Parcel arrived smashed" ticket would now come out as `queue: None, urgency: None, summary: "Parcel arrived smashed", stand_ins: ["queue", "urgency", "summary"]`. The opening-hours ticket has `stand_ins: []`. Show the "check me" marker whenever `stand_ins` is non-empty.

**Other files**
- **Tests:** `test.py` replaces the three old "falls back to general/normal" tests with null-and-flagged equivalents, plus one for a missing summary.
- **README:** `README.md` documents the new behaviour.
- **Charter:** `evals/triage_ticket/charter.md` is untouched.

**Check before deploying:** anything downstream that reads `queue` or `urgency` must now handle `None`. Routing code that assumed a string, or that did a lookup on `respond_within_hours`, will need to cope with it.