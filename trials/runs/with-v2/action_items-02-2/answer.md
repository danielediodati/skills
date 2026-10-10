Weekday deadlines are now explained to the model in the prompt, so "by Friday" should come back as a date instead of an empty due. I haven't run it against a real model, so your Ana/Tom/Priya example is not confirmed end to end. The 18 unit tests pass, including a new one that checks the prompt contents.

**What changed (`seam.py`)**
- The prompt now states the meeting's weekday, for example `2026-03-03 (Tuesday)`. The model no longer has to work out the weekday of a date itself.
- The `due` instructions now say that a weekday is a deadline, counted from the meeting:
  - "by Friday" is the first such weekday after the meeting.
  - "by next Friday" is that weekday in the following week.
  - If the meeting falls on that weekday, "by Friday" means a week later.

**Why in the prompt and not in code:** the charter lists "what deadline the notes mean" as the model's decision. Resolving weekdays in code would have taken that over and moved the line. The prompt only gives the model criteria and a fact, so the decision stays with it. The existing checks still apply: a real date, on or after the meeting. The charter is untouched.

**Sorting:** this should fix the sinking to the bottom, because those tasks now carry a date and the existing sort puts dated items first by deadline.

**Left alone:** the charter marks some behaviours as "not yet in code" (the 10-item cap, and a rejected due date looking the same as none). They aren't part of this request, so I didn't change them.