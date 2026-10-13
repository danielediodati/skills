I made the part of the fix that can be made without moving a line, and stopped short of the rest. Nothing paid was run.

**What changed (`seam.py`, prompt only)**
- The prompt now says numeric dates may be day-first or month-first, and tells the model to decide from what the invoice shows. That covers supplier country and address, currency, language, other dates, and any date with a number above 12.
- If nothing on the invoice settles it, the model returns `null` instead of guessing. Your existing required-field check then rejects it with `issue_date is missing`, so a clerk handles it and it never reaches the ledger looking certain.
- I added a test for that path. The 15 tests pass.

**What this does not do**
- It is only a prompt change, so it can't guarantee that 05/08/2026 from Brightwell now comes out as 5 August. I have not measured it. A paid run on a small set of day/month-ambiguous invoices, including BP-2304 and the American 03/04/2026 one, would tell you; I need your approval and a budget before running anything.
- It rejects the invoice outright rather than loading it with a "date doubtful" flag.

**The line I did not move**
Loading the invoice while marking its date as doubtful would need a new output key or a new `status` value. The charter fixes the output keys and makes `status` `ok` or `mismatch` only, based on the total. Changing either is your decision, and it would also touch the downstream ledger loader. What it would buy: invoices with an uncertain date reach a clerk with all their other fields filled in, instead of being bounced for re-entry.

Do you want to keep rejection as the behaviour, or change the output contract to carry a flag?