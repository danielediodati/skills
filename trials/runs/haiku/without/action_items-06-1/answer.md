Deadlines said in meeting language now resolve against the meeting date. For Tuesday 3 March, "by Friday" gives 6 March and "by the end of next week" gives 13 March. The unit tests pass (22 of 22).

**Cause:** The prompt asked the model to write every deadline as `YYYY-MM-DD`. The code kept only real ISO dates and had no way to interpret "Friday". So the model did the calendar arithmetic itself, and got it wrong for Ana (5 March) or left Tom's undated.

**Changes in `seam.py`:**
- The prompt now asks for a date as `YYYY-MM-DD`, but if the notes give a weekday or relative phrase, the model copies that phrase as spoken.
- A new `_resolve_phrase` turns those phrases into dates in code:
  - A bare weekday ("Friday", "Tuesday") is the next such day, counting the meeting day itself.
  - "next Monday" is the Monday of the following week.
  - "end of this week" and "end of next week" are the Friday of that week.
  - Any other phrase, such as "in two weeks", stays `None` rather than being guessed.
- A leading "by" and "the" are ignored.

**Tests in `test.py`:** I added cases for each phrase type, plus one that uses your three meeting deadlines. The "end of next week" case is the one that was failing for Tom.

**README:** The deadline rule now mentions that weekday and relative phrases are resolved in code.

**Choices to check:**
- "next Friday" means the Friday of the following week. Some people would read it as the next Friday, so tell me if your team uses it that way.
- A bare "next week" is not resolved, so it stays undated. I chose that over guessing which day it means.

The tests use a fake model, so they don't show how the real model behaves. Run a few real meeting notes through it to confirm the model copies phrases like "by Friday" rather than converting them to dates itself.