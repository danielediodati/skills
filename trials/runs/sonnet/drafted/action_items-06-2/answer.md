I changed the prompt so the model has what it needs to get those deadlines right. The local tests pass, but I haven't confirmed the fix against a real model, because that needs a paid call.

**Likely cause:** the prompt gave the model the meeting date (`2026-03-03`) but not that it was a Tuesday, and said nothing about how to read "by Friday" or "end of next week". So the model had to work out the weekday itself, which is how you got Thursday 5 March. And it had no reason to turn a vague "end of next week" into a date, so it wrote `none` for the venue.

**What I changed in `seam.py`:**
- The prompt now states the weekday: "held on 2026-03-03, a Tuesday".
- The `due` instructions now say:
  - Work relative deadlines out from the meeting's date and weekday, with weeks running Monday to Sunday.
  - "By Friday" means that Friday itself, not the day before.
  - "End of next week" means the last working day of the week after the meeting's week.
  - Write a date whenever the notes give a deadline, and `none` only when they give none.
- I added a test in `test.py` that the prompt carries the weekday.

**Why only the prompt:** the charter lists the deadline's value as the model's decision and says code does no date arithmetic on natural language. So I left the parsing, the "on or after the meeting date" check and the sorting alone, and did not touch the charter. The new wording informs the model's judgement rather than dictating an answer.

**Not yet verified:** a real model might still misread your three lines. Checking that means running your 3 March notes through the model: one call per run, and your meeting is a ready-made case. Nothing paid has run. If you want me to do it, tell me which model and a spending budget for this ticket, and I'll run it and show you the three resulting deadlines.

**Related, outside this fix:** you said you can't tell which dates to trust. The seam turns any unreadable or past deadline into `None` silently, so a wrong-but-valid date such as the Thursday looks the same as a right one. Code can't check that without doing date arithmetic on the notes, which the charter reserves for the model. If you want deadlines flagged for review, that is a decision for you about the charter.