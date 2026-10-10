Weekday deadlines now get resolved to dates. The 19 tests pass, including two new ones. I haven't run it against a real model, so the end-to-end behaviour depends on the model following the table.

**Cause:** the model has to write the due date. The prompt gave it only the meeting date, with no weekday and no rule for "Friday" or "next Wednesday". It either answered `none` or guessed, and the code then dropped anything unreadable or before the meeting.

**Fix in `seam.py`:** the code now does the calendar arithmetic and puts the result in the prompt as a lookup table. The model only has to choose a row. For your example meeting (Tuesday 3 March 2026) the table looks like this:

```
Wednesday: by = 2026-03-04, next = 2026-03-11
Friday:    by = 2026-03-06, next = 2026-03-13
```

- **"by Friday":** the first such day after the meeting, never the meeting day itself. A meeting on a Friday gives a week later.
- **"next Wednesday":** that day in the calendar week (Monday to Sunday) after the meeting's own week. For your example that gives 11 March.
- **Prompt:** the meeting's weekday is now stated, and the prompt says a day of the week counts as a deadline. Explicit dates are used as written.

**Tests added in `test.py`:** the table for a Tuesday meeting, and the Friday meeting case (Friday and Monday both a week ahead).

Decision for you: when the meeting falls on the same weekday as the one named, "next Tuesday" at a Tuesday meeting resolves to the following Tuesday, 10 March, the same as plain "Tuesday". If you'd rather "next" mean 17 March there, it's a one-line change.