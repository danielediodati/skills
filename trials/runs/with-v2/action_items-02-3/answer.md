I changed the prompt in `seam.py` so day-of-week deadlines are read as dates. The 18 tests pass, but they use a fake model, so I haven't run it against a real one with your example notes.

**Why it was failing:** the prompt only asked for "the deadline as YYYY-MM-DD". Given "by Friday" and a bare date, the model had no weekday for the meeting and no rule for resolving the day, so it often answered `none`.

**What I changed:**
- **Meeting weekday:** the prompt now says the meeting was held on "Tuesday 2026-03-03", so the model doesn't have to work out the weekday itself.
- **Reading rule:** the prompt now tells the model that a day of the week is a deadline. "By Friday" is the first Friday after the meeting, and "by next Friday" is the Friday of the following week. A Friday meeting's "by Friday" means a week later.
- **Test:** I added one test that checks the weekday appears in the prompt.

**Where the line stays:** the charter lists "what deadline the notes mean" as the model's decision, so I added no weekday-to-date code and left the charter untouched. The existing check still discards any date before the meeting.

**Open risk:** the fix depends on the model following the rule. If it still gets "next Wednesday" wrong, the remedy would be code that resolves weekdays itself, which would take that decision away from the model. That is your call, since it moves the charter's line.