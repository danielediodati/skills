I made only part of the fix, because the cause of your problem is a rule the charter keeps in code, and only you can change it.

**Cause**

The model's own urgency is not what pushes the invoice copy into urgent. The enterprise raise is: it adds one level after the model answers (`seam.py:47-50`). Anything the model calls `high` becomes `urgent`, which carries the one-hour deadline and the page. A real outage is `urgent` before the raise and stays `urgent`, so the two end up identical.

**What I changed**

I added definitions of the four urgency levels to the prompt in `seam.py`. They say urgency is how soon the customer is hurt, not how important the customer is. "Urgent" is described as broken right now with no workaround. Invoice copies, how-to questions and adding a user are described as `normal`.

- **Charter fit:** this only gives the model criteria for a decision the charter already lists as free. It does not move a line.
- **Tests:** the local unit tests pass (11 of 11).
- **Not measured:** I have not checked how the model's ratings change, because that needs paid runs and I haven't asked you for a budget.
- **Limit:** this alone won't fix it. A high-rated enterprise ticket still lands in urgent.

**The line I stopped at**

The charter marks two things as constrained: the enterprise raise, which is a contractual promise applied in code, and the urgent-means-1-hour table. Fixing this properly means changing one of them, and I'm leaving that decision to you. The options:

1. **Cap the enterprise raise at `high` (recommended).**
   - Enterprise tickets would move from 24h to 8h, and from 8h to 8h, so only a real urgent gets the page.
   - Cost: an enterprise `high` gets no faster than 8h. You'd need to check that against what the contracts say.
2. **Add a fifth level between `high` and `urgent`**, for example `priority` with a 2-hour answer. Enterprise tickets would raise into it.
   - This keeps a faster-than-ordinary promise and still separates the two kinds of ticket.
   - It changes the closed urgency set and the hour table, and the desk's routing and paging would need to know the new level.
3. **Keep urgency as the model's own judgment and carry enterprise as a separate flag the desk sorts on.**
   - The list and paging would use both fields. The one-hour promise would then apply only to real urgents.
   - This changes the output shape and the contractual raise.

The charter would need updating for any of these, and that edit is yours to make. Tell me which you want and I'll implement it, with tests.

If you want to measure the prompt change first, I'd propose a small budget for one run of a few dozen labelled tickets against the cheapest model, but nothing paid has run yet.