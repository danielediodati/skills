I changed the prompt so the model reads relative deadlines off a calendar instead of counting days. The unit tests pass, but I haven't run it against a real model, so I haven't confirmed your March example comes out right.

**Cause:** the code never computes dates. The model does, and it was only given `2026-03-03` with no weekday and no convention for "by Friday" or "end of next week". It had to work out that 3 March is a Tuesday by itself, which is how Ana's Friday became Thursday. It treated Tom's "end of next week" as too vague to date, so it returned `none`. Exact dates like "10 March" need no calculation, which is why those were always right.

**Changes in `seam.py`:**
- The prompt now states the weekday of the meeting ("Tuesday 2026-03-03").
- It includes a 15-day calendar starting on the meeting day, so every weekday maps to a date.
- It sets out the rules for turning spoken deadlines into dates:
  - "by Friday" is the first Friday after the meeting day.
  - "end of this week" or "end of next week" is the Friday of that week.
  - "next Monday" is that weekday in the week after the meeting's week.
  - "tomorrow" is the day after the meeting.
  - "none" is only for notes that give no deadline at all.

For your meeting the calendar shows Friday 6 March and Friday 13 March, which are the dates you wanted for Ana and Tom.

**Tests:** I added a test in `test.py` that checks the weekday, both Fridays and the "end of next week" rule are in the prompt. All 18 tests pass.

**Conventions you may want to change:**
- If the meeting is on a Friday, "by Friday" resolves to the following Friday, not that day. Say if you'd rather it meant the same day.
- "End of the week" is treated as Friday, not Sunday.

Because the model still does the final mapping, I'd run this on your actual notes from 3 March to confirm. Anything it can't date will still come out as `none`, and the existing checks in the code (dates before the meeting are dropped, bad formats become `none`) are unchanged.