Weekday deadlines should now reach the model with enough context to be dated. I haven't run a real model on your example, only the unit tests, which pass (18).

**What I changed**
- `seam.py`: the prompt now says the weekday of the meeting (e.g. "Tuesday 2026-03-03") and lists the 14 days after it as a small calendar.
- The prompt also states your rule:
  - "by Friday" is the first Friday after the meeting.
  - "by next Friday" is the Friday of the following week.
  - If the meeting is on that day, it means a week later, never the same day.
- `test.py`: a new test checks that the prompt carries the weekday, the calendar dates (`Friday 2026-03-06`, `Wednesday 2026-03-11`) and the "next" rule.

**Why the fix is in the prompt and not in code**
- The charter lists "what deadline the notes mean" as the model's call, so I kept that with the model. The line hasn't moved, and the charter is unchanged.
- The cause was in the prompt: the model got a bare ISO date with no weekday and no guidance. It also had to do weekday arithmetic unaided, which is unreliable.
- The existing code rules still apply: a date before the meeting becomes `None`, and dated items sort first.

**Worth knowing**
- Your example expects "next Wednesday" from Tuesday 3 March to be 11 March, so I wrote "next X" as "X in the following calendar week". By that rule "next Friday" from that Tuesday is 13 March, not 6 March. If your people mean something else by it, say so and I'll adjust the wording.