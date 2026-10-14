The deadlines were wrong because the model was misreading relative dates, and the code never checked them. I changed the prompt so the model has a rule for reading them. I have not yet confirmed that the model now gets Ana's and Tom's dates right.

**What was wrong:** "by Friday" and "end of next week" are read by the model, which writes a `YYYY-MM-DD` date. The code only checks that the date is valid and not before the meeting. So a wrong date passed straight through, and "end of next week" came out as no deadline. The charter lists this reading as the model's decision, so a date parser in code would have taken it over.

**What I changed:** `seam.py`, in the prompt's `due:` bullet. It now says a relative deadline is a calendar date counted from the meeting date:
- "by Friday" is the first Friday on or after that date.
- "next week" is the week after the meeting's week.
- "end of next week" is the Friday of that week.

For your meeting, that gives Ana's quote as Friday 6 March and Tom's venue as Friday 13 March. I checked those weekdays. The model still decides the dates, and the code still only validates them, so no line moved. The prompt text is one the charter lists as constrained, so please look at that wording.

**Tests:** I added a test in `test.py` that checks the prompt contains the rule. All 18 tests pass. That covers the prompt text only. It doesn't show that the model follows the rule.

**Not done:** I haven't run the real model on your 3 March notes. That is a paid call, so I need your approval first. Per `AGENTS.md`, I'd also agree one spending budget for the whole ticket before the first paid call. My suggestion is a single run on those notes, and I'd show the running total against the budget before any further runs. Tell me the budget and I'll run it. I haven't edited the charter.