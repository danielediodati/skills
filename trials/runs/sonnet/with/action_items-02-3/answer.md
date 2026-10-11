Day-of-week deadlines now go through the prompt, so the model resolves them and they should land in the due column and sort correctly. The 18 existing tests pass. I did not run it against a real model, so the three-line example from your report is untested end to end.

**Why the prompt, not code:** the charter (`evals/action_items/charter.md`) lists "what deadline the notes mean: turning 'by Friday' into a date" as a free decision for the model. A weekday parser in code would have moved that line. The prompt had no guidance on this, so the model left the due date as "none" and the code kept it that way.

**Changes in `seam.py`:**
- The prompt now states the meeting's weekday alongside its date ("Tuesday 2026-03-03"). Models are unreliable at working out weekdays from ISO dates.
- The `due` instruction says a weekday counts as a deadline:
  - A bare weekday is the first such day after the meeting, never the meeting day itself.
  - "Next <weekday>" is that weekday in the week after the one the meeting falls in.
  - The prompt includes your example: "Friday" → 2026-03-06, "next Wednesday" → 2026-03-11.
- The weekday name comes from a fixed tuple rather than `strftime`, so it does not depend on locale.

**Test:** `test.py` has a new test that the prompt carries the weekday and the rule.

Because the model does the date arithmetic, an occasional wrong date is possible, and code can't catch one that is still on or after the meeting. If you want a regression check, a few real-model cases covering "Friday", "next Wednesday" and a Friday meeting saying "by Friday" would be the place to add it.