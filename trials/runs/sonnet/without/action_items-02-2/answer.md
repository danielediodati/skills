Day-of-week deadlines now get a due date, and the list sorts them in with the dated items. All 21 tests pass, including four new ones.

Changes in `seam.py`:

- **Prompt:** it now gives the meeting's weekday and the rule for "by Friday" and "by next Wednesday". It also lists the next 14 days with weekday and ISO date, so the model doesn't have to do the calendar arithmetic itself.
- **Parser:** if the model returns a weekday phrase instead of a date (`Friday`, `by Friday`, `next Wednesday`, `on Monday`), the code resolves it. This covers a model that ignores the prompt.

The resolution rules:

- **Plain weekday:** the first such day strictly after the meeting, so a Friday meeting with "by Friday" gives the Friday a week later.
- **"next" weekday:** that weekday in the following Monday–Sunday week. For your Tuesday 3 March example, Friday is 6 March and next Wednesday is 11 March.

The new tests are in `test.py` and cover those rules, the Friday-on-Friday case, and the calendar in the prompt.

One ambiguity to be aware of: "next Friday" said on a Tuesday resolves to 13 March, not 6 March. That follows your "the one in the following week" rule, but people sometimes mean the nearer one.