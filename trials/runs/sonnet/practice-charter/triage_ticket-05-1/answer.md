`triage_ticket` now says which tickets came back without a real verdict. All 13 tests pass.

**What changed**
- **New field:** the result has a `fallback` list naming the fields that were defaulted: `queue`, `urgency` and/or `summary`.
- **Reading it:** an empty list means the model gave a valid answer for all three. A non-empty list means the ticket arrived without a real verdict, like your "Help!!" ticket.
- **Genuine general tickets:** a ticket the model really judged `general` / `normal` has `fallback: []`, so it no longer looks the same as a defaulted one.
- **Unchanged:** the values, the SLA mapping, the single model call and the enterprise raise are exactly as before. Each defaulted field is recorded before the tier raise, so an enterprise ticket whose urgency was defaulted is still flagged.
- **Files:** the change is in `seam.py`, with new tests in `test.py` and a README entry. The charter is untouched. It already listed this gap as "not yet in code", so closing it moves no line.

**One caveat**
Your ticket-list UI isn't in this code, so I couldn't make the list itself show the flag. Whatever renders the list needs to read `fallback`, for example to show a "needs a person" badge or sort those tickets first. Any consumer that compares the result dict for exact equality will also see the extra key.

**What this won't catch**
If the model answers validly but wrongly, say `general` / `normal` for the warehouse outage, `fallback` stays empty. Catching that would mean second-guessing the model's judgment in code, which the charter reserves to the model. If that happens often, it's a decision for you about the charter rather than something I should change.