I changed the prompt in `seam.py` so the model now resolves "by Friday" and "by next Wednesday" to dates. I haven't run it against a real model. The 17 existing tests pass, but they use a canned fake model, so they don't exercise the new wording.

**Cause:** the prompt only said "the deadline as YYYY-MM-DD, or none if no deadline was given". It never said a weekday counts as a deadline, so the model returned `none` for "by Friday", and an undated item sorts to the bottom.

**What I changed:**
- The prompt now states the meeting's weekday next to its date, e.g. "2026-03-03 (Tuesday)". Models are unreliable at working out weekdays from ISO dates.
- It tells the model that a weekday is a deadline: "by Friday" is the first such day after the meeting, and "next Wednesday" is that weekday in the following week.
- If the meeting falls on that same weekday, the date meant is a week later, not the meeting day.

**Charter:** "What deadline the notes mean" is listed as free, so the model keeps that decision and code does not compute the date. I added criteria to the prompt rather than a resolver, and I didn't touch the charter.

**Not covered by a test:** your example should now come out as 6 March and 11 March. I didn't add a test for it, because with a fake model it would only check the canned answer. A check against a real model on your example notes would confirm the fix.