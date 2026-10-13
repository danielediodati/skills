Relative deadlines are now resolved in code instead of by the model. I couldn't run the test suite, because shell access was denied partway through this session, so none of it has been executed. I traced the new tests by hand against the 3 March meeting and they come out as expected.

**Cause**

The prompt asked the model to turn "Friday" or "end of next week" into a `YYYY-MM-DD` date. Language models are unreliable at that arithmetic: it picked Thursday 5 March for "Friday", and for "end of next week" it gave something the code threw away. The code then accepted any real date on or after the meeting, so a wrong date looked the same as a right one. Dates you wrote as `10 March` worked because the model only had to copy them.

**Changes**

- **`seam.py`, prompt:** the model now writes `YYYY-MM-DD` only when the notes give a calendar date. When the notes say it in words, it copies the words exactly and doesn't work out the date.
- **`seam.py`, `_parse_due`:** an ISO date is used as before. Anything else goes to a new `_resolve_phrase`, which computes the date from the meeting date. A phrase it doesn't understand becomes no deadline, as before.
- **`test.py`:** new `SpokenDeadlineTest` covers your three deadlines (6 March, 10 March, 13 March) plus weekdays, "next Friday", "tomorrow", "in two weeks", "end of the month" and an unknown phrase.
- **`README.md`:** documents the behaviour.

**Conventions I chose**

These are judgment calls, so check they match how your team talks:

- Weeks run Monday to Sunday, and "end of the week" means that week's Friday.
- A bare weekday is its next occurrence after the meeting day: "by Friday" on a Tuesday is that week's Friday. "By Tuesday" said on a Tuesday means the following Tuesday.
- "Next Friday" means Friday of the following week (13 March here). Some people mean the nearest Friday, so this is the likeliest one to disagree with you.
- A bare "next week" is treated as the end of next week (its Friday), because a deadline of "next week" usually means by then.

**To do**

Please run `python -m unittest` in the project directory to confirm.

**Limitation**

This only fixes the failure when the model copies the phrase as asked. If it ignores the instruction and writes a wrong ISO date, the code can't tell. If you still see stray dates, the next step is to have the model return the verbatim phrase in a separate field, so the code never has to trust a model-written date for spoken deadlines.