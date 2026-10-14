I haven't changed any code. The fix you want would move a line the charter reserves to the model or to you, so the decision is yours.

**Why it happens:** The charter (`evals/extract_invoice/charter.md`) lists "date format as read" as free. The model reads "05/08/2026" as 8 May, and the code's only check is `date.fromisoformat`. Both 5 August and 8 May are valid calendar dates, so the check cannot catch the swap. The same applies to the American "03/04/2026" case. The charter treats a wrong date as something code can't see, so nothing marks it as doubtful.

**Options, with the line each one moves:**

1. **Tell the model the day-first convention for British and European suppliers in `PROMPT`.** This changes the fixed prompt wording, and the charter says code must not dictate how the date is read. It also would not reliably fix the American case, because the model would have to infer the supplier's country.
2. **Ask the model for the date as printed as well as the ISO date, then have code flag ambiguous dates for a clerk.** An ambiguous date is one where both day and month readings are valid. This adds a key to the output, which the charter calls a contract change, and adds a new constraint. Code can flag the ambiguity but cannot pick the right reading on its own, so a clerk still resolves the date.
3. **Have code parse the printed date from a supplier-country field.** This takes the date reading away from the model, which the charter lists as free, and adds a new constraint.

I'd recommend option 2. It stops a guessed date from looking as certain as the others, and it doesn't depend on the model knowing the supplier's country. The charter needs to record it before any code changes, and only you can change the charter.

**Verification:** The 14 existing unit tests pass (`python -m unittest`). I made no model calls, so nothing was spent.

Which option do you want? If it's option 2, please update the charter first and I'll make the change and add tests for the ambiguous-date case.