The result now says which fields are stand-ins, and all 13 tests pass.

**What changed in `seam.py`**
- **`stand_ins`:** a new list in the result naming the fields that were not the model's own judgement, from `queue`, `urgency` and `summary`. It is empty when the model answered all three, so "check me" is simply `stand_ins != []`.
- **Null instead of defaults:** a queue or urgency the model didn't give validly is now `null`, no longer `general` or `normal`. `respond_within_hours` is `null` when the urgency is `null`. This is what the charter already specified ("Not yet in code"), so no line moves.
- **Summary:** it still falls back to the subject, which the charter allows, but is now listed in `stand_ins`.
- **Enterprise tier:** a `null` urgency is not raised and stays `null`.

"Parcel arrived smashed" would now come out as `queue: null`, `urgency: null`, `summary: "Parcel arrived smashed"`, `stand_ins: ["queue", "urgency", "summary"]`, while the opening-hours ticket stays `general` / `normal` with an empty list.

**Check before you ship:** anything that reads `queue`, `urgency` or `respond_within_hours` must now handle `null`. The ticket list and any "general queue" filter will otherwise drop these tickets or break on them.

I updated the README and the tests to match. I did not touch the charter.