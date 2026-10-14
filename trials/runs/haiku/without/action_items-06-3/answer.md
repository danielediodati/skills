Deadlines now come out as you agreed them in the room: Ana's quote on Friday 6 March, Tom's venue on Friday 13 March, and Priya's badges on 10 March. All 21 tests pass.

**The cause:** the prompt asked the model to convert each deadline to a calendar date itself. The model got "by Friday" wrong, and the code accepted any valid date, so the wrong one went through. Tom's "by the end of next week" had no date to convert, so it came out as `none`.

**The change:**
- **`seam.py`:** the prompt now asks for the deadline in the notes' own words and tells the model not to work out a date. The code resolves the phrase against the meeting date:
  - A weekday means the first such day on or after the meeting, so "Friday" on Tuesday 3 March is 6 March.
  - "End of next week" means the Friday of the following Monday–Friday week, so 13 March.
  - Day and month forms like "10 March", "March 10th", "the 6th" and "10 Mar" are also handled.
  - Anything else, or a date before the meeting, stays `None` as before.
- **`test.py`:** new tests cover weekdays, "end of next week", the day-and-month forms, and unresolvable phrases.
- **`README.md`:** updated to describe the new behaviour, and the example now says "by Friday".

**Choices you may want to change:**
- A weekday said on the meeting day itself resolves to that same day.
- "Friday the 6th" is not handled and becomes `none`. Tell me if your notes use that form often.

**Not verified:** I checked the parser with a stand-in model that copies the wording from the notes. I have not run it against the real model, so check that its output matches the phrases the prompt asks for.