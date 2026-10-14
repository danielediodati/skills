The prompt now gives the model the meeting's weekday and the next two weeks with their weekdays, so "by Friday" and "by the end of next week" can be resolved against the real calendar. The existing 17 tests pass, plus one new test for the prompt, 18 in all. I have not confirmed that the model now returns 6 and 13 March, because that needs a paid model call, and I haven't made one.

**What changed (`seam.py`, `test.py`)**
- The header now reads "held on Tue 2026-03-03", and the prompt lists the 14 days from the meeting day with their weekdays.
- The due-date instruction now says a relative deadline such as "by Friday" or "by the end of next week" is converted using those days.
- The date conversion is still the model's job, as the charter says. The code only adds the calendar as information. Nothing in the code computes a deadline, so no line moved.
- I did not edit `evals/action_items/charter.md`.

**What I checked**
- Tests: 18 pass with `python -m unittest`.
- The prompt for your Tuesday 3 March notes includes `Fri 2026-03-06` and `Fri 2026-03-13`, so the model has both dates to choose from.

**What I did not check**
- Whether the model picks 6 March for Ana and 13 March for Tom. The charter says paid runs need your approval and a budget for the ticket first. I can set up a small eval over your meeting notes once you agree a budget.
- "End of next week" is ambiguous, so the model could still pick a different Friday or Monday. The eval would show that.
- Deadlines beyond the 14-day calendar rely on the model alone.

No commit was made; this directory is not a git repository.