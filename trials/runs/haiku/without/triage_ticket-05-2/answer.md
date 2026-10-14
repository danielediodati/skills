Tickets that the model couldn't triage are now marked, so they stand out in the list from the ones that really were judged general and normal.

**What changed in `seam.py`**
- `triage_ticket` records each field that fell back to a default (`queue`, `urgency`, `summary`) in a new `fallbacks` list.
- It adds `needs_review`, which is `True` whenever `fallbacks` is not empty.
- A real verdict of `queue: general` / `urgency: normal` is not flagged. That was the distinction you asked for.
- The existing fields keep their meaning, so the ticket list won't break. The two new keys are additive.

**Tests and docs**
- I updated the two tests that compare the whole dict, and added tests for the fallback cases and for a genuine general verdict that must stay unflagged.
- `python -m unittest` runs 13 tests and all pass.
- `README.md` documents the two new fields.

**What it won't catch**
This only flags tickets where the model's answer was unusable or missing. If the model answers confidently with `general` / `normal` for a warehouse outage, the ticket still looks ordinary. I don't know which of those happened on the Tuesday ticket, and a fallback flag wouldn't have caught a confident wrong answer. A cheap complement would be a keyword check on the body for words like "down", "can't print", "since", "orders waiting" that forces `needs_review` or raises urgency. I didn't add that because it's a product decision about what counts as urgent. I can add it if you want.

**Decision for you:** the ticket list needs to show `needs_review` somewhere, and this repo doesn't include that UI. Whoever renders the list should sort or highlight tickets where `needs_review` is true.