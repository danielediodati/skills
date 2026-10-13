I changed the prompt so the model can resolve "by Friday" and "end of next week" against the real calendar. I have not run it against a live model, so I can't yet confirm that your March notes now come out as the 6th and the 13th.

## Likely cause
The prompt gave the model only `2026-03-03`, with no weekday. It had to work out that this was a Tuesday itself, and a model that gets that wrong lands on Thursday for "Friday". For "end of next week" it had no anchor at all, so it often answered `none`. Calendar dates like "10 March" never needed any of this, which is why those came out right.

## What changed (`seam.py`, `test.py`)
- **Weekday:** the prompt now says "a meeting held on Tuesday 2026-03-03".
- **Calendar:** it lists the next three weeks, weekday and ISO date per line, so the model looks dates up instead of computing them.
- **Instruction on `due`:** phrases like "by Friday" and "end of next week" are deadlines and should be resolved against that calendar.
- **Tests:** a new test checks that the prompt contains Tuesday 3 March, Friday 6 March and Friday 13 March. All 18 tests pass.

## Charter
This stays inside the charter. The deadline's value is still the model's decision, and I added no resolution in code. The weekday and calendar are reference information, not a rule that picks the answer. Because the model still decides, a wrong date is still possible. The charter's checks (real date, not before the meeting) are unchanged.

I did not edit the charter.

## Next step
Checking this means a live run on your March notes (one model call per run, plus a few runs to see how stable it is). That is paid, so I need your approval and a spending budget for this ticket before I do it. What model and budget would you like?