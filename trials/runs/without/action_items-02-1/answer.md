Weekday deadlines are now resolved to dates. All 22 tests pass, including the new ones for your example.

**Cause:** the prompt told the model to answer with `YYYY-MM-DD`. Models are unreliable at date arithmetic, so "Friday" often came back as `none`, or as something the code then discarded. The task kept its owner and lost its due date, and the sort put it at the bottom.

**Fix (`seam.py`):**
- **Prompt:** when the notes give only a weekday, the model now writes it as said ("Friday", "next Wednesday") and does no date maths.
- **Resolution in code:** `_weekday_due` turns the weekday into a date from the meeting date.
  - A bare weekday is the first such day after the meeting, so a Friday meeting with "by Friday" gives a week later.
  - "next X" is that day in the following calendar week, Monday to Sunday.
  - Abbreviations ("Fri", "Wed") and a leading "by", "on", "before" or "until" are accepted.
- **Unchanged:** the existing checks still apply, so an unrecognised word still becomes no deadline.

**Result for your example (meeting Tuesday 3 March 2026):** Friday gives 6 March, next Wednesday gives 11 March, and 20 March stays as is. The list sorts in that order.

**Tests and docs:** I added tests in `test.py` and a line in `README.md` describing the rule.

**Your call on "next":** I read "next" as the following calendar week, as you described it. So "next Monday" said on a Friday is three days later, not ten. If you would rather it always mean the first such day plus seven days, it is a one-line change in `_weekday_due`.