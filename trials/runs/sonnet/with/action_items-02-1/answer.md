I changed the prompt so the model is told how to read weekday deadlines. The 18 tests pass, but they use a fake model, so I haven't checked that a real model now returns the dates in your example.

**Cause:** the prompt gave the model only `2026-03-03` and asked for a `YYYY-MM-DD` date. It never said that "by Friday" counts as a deadline or which Friday it means. With the weekday not even stated, the model often answered `none`, and the item went to the bottom of the list.

**Changes in `seam.py`:**
- The prompt now states the meeting's weekday, for example `2026-03-03 (Tuesday)`.
- It now says that a day of the week is a deadline.
- "By Friday" means the first Friday after the meeting, and a week later if the meeting is itself on a Friday.
- "By next Friday" means the Friday of the following week.

**Test:** `test.py` has a new check that the prompt carries the weekday and these rules.

**Charter:** I left it unchanged. "What deadline the notes mean" is listed as free, so turning a weekday into a date stays with the model. I did not add weekday parsing in code, because that would take the decision away from the model and move the line. The existing checks still apply: a date before the meeting becomes `None`, and dated items sort first.

To confirm the fix, run your March 3 example against a real model and check that the due dates come out as 6 March and 11 March.