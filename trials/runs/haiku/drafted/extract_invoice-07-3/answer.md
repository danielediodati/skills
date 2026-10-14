**Stuck:** I haven't changed the date handling. Fixing the day/month swap needs a change to the prompt template or the output contract, and the charter puts both on the constrained side. You need to decide that.

**What the charter says**
- Reading dates such as "02/10/26" into YYYY-MM-DD is **Free**: "the model reads the document's conventions." The Brightwell error is the model's reading, not a code bug.
- The prompt is **Constrained**: "fixed template, with the whole invoice inserted as-is… Tightness: exact."
- Code cannot fix this. It can't tell 05/08 from 08/05, so any code rule that picks an order takes the decision from the model. That moves the line.

**Options, each of which moves a line**
1. **Tell the model about day-first and month-first conventions in the prompt.** This is the most likely fix. Guidance such as "dates may be day-first or month-first; use the supplier's country and currency" informs judgement and is allowed in principle. But it edits the constrained template, so it needs your approval and a charter change.
2. **Add a date-confidence field to the output** so a guessed date is flagged for a clerk. This changes the output contract in the charter and asks the model for a new judgement. It also needs a charter change.
3. **Check `issue_date` against the invoice text in code.** This adds a constraint to a free decision and cannot say which reading is right, so it only partly meets your need.

**Current state**
- I ran the local tests: 14 pass. They don't cover ambiguous dates; the only date fixture is "2 Oct 2026", which is unambiguous.
- I made no paid calls. Checking option 1 against Brightwell BP-2304 and the American "03/04/2026" invoice would need a model run, so I'd need your approval and a spending budget for this ticket first.

If you want option 1, tell me to proceed and say whether you'll update the charter yourself. I won't edit the charter. Otherwise I can leave the seam as it is.