Ana's quote now comes out as Friday 6 March and Tom's venue as Friday 13 March. All 24 tests pass, including the new ones for these phrases.

**What was wrong**

The prompt told the model to write every deadline as `YYYY-MM-DD`, so it had to do the calendar arithmetic itself, and models get that wrong. "By Friday" came out as the Thursday. "End of next week" wasn't a date the model could settle on, so it wrote `none`. The code then discarded anything it couldn't read as a date, so Tom's task dropped to the undated group without any warning.

**The fix** (`seam.py`)

- **Prompt:** calendar dates in the notes are still written as ISO dates. Relative wording ("Friday", "end of next week", "in 3 days") is copied exactly as it appears in the notes, and the model no longer works out the date.
- **Code:** a new `_resolve_relative` turns those phrases into dates from the meeting date, so the result is the same every time.

**How phrases resolve** (weeks run Monday to Sunday)

| Phrase | Result for a Tuesday 3 March meeting |
|---|---|
| `Friday`, `by Friday` | Fri 6 March |
| `Tuesday` (same weekday as the meeting) | Tue 10 March, a week later |
| `next Friday` | Fri 13 March |
| `end of the week` | Fri 6 March |
| `end of next week`, `next week` | Fri 13 March |
| `tomorrow`, `today`, `end of day` | 4 March, 3 March |
| `in 2 weeks`, `in three days` | 17 March, 6 March |

**What to know**

- **"Next Friday":** I read "next Friday" said on a Tuesday as the Friday of the following week (13 March). Some people mean the nearest Friday, so say if your team uses it that way.
- **Unrecognised phrases:** a phrase the code doesn't recognise, such as "once the budget is approved", still ends up undated, as before. That is now the only way a relative deadline loses its date, and it's easy to extend.
- **Model compliance:** the fix depends on the model following the new prompt wording. If it still writes an ISO date for "Friday", that date will be used as given, so spot-check a real run once.
- **README:** I didn't update it. Its example still shows "Friday the 6th", which works fine because that is a calendar date.