A ticket whose triage didn't produce a usable answer now says so, field by field. All 13 tests pass.

**What changed in `seam.py`**
- **Queue and urgency:** a queue or urgency the model didn't give validly is now `None` instead of `general` / `normal`. The "Parcel arrived smashed" ticket would come out with queue `None` and urgency `None`, not look like a normal general ticket. The enterprise raise is skipped when urgency is `None`, and `respond_within_hours` is `None` with it.
- **Summary:** it still falls back to the subject line, since the charter allows that, but it is now flagged.
- **`stand_ins`:** the result has a new `stand_ins` list naming which of `queue`, `urgency` and `summary` are not the model's judgement. It is empty when the triage is complete, so "check me" is `bool(result["stand_ins"])`.

**Other changes**
- **Charter:** it already specified `null` instead of defaults and noted "Not yet in code". This brings the code in line with it and leaves the charter untouched.
- **Tests and README:** tests are updated and extended, and the README is updated.

**One thing to handle on your side:** anything that read `queue` or `urgency` and assumed a string, or used `respond_within_hours` as a number, now has to cope with `None`. The ticket list should show those as "unclassified" along with the marker.