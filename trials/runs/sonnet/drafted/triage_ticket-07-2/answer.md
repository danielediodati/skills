I haven't changed anything, because the fix means moving a line in the charter that only you can move.

**Cause.** In `seam.py:47-50`, every enterprise ticket is raised one urgency level after the model's judgement, capped at `urgent`. The model rates "Copy of August invoice" as `normal` or `high`, and the bump makes it `high` or `urgent`. That maps to a 1-hour deadline, and that deadline is what pages you. The model isn't misjudging anything. The charter lists this rule under *Constrained* ("a contractual promise, not a judgement"), and the response-hours table is constrained too. So I can't change the bump, cap it, or reshape the deadlines without moving that line, and I can't ask the model to compensate for it.

**What moving it would buy.** `urgent` would go back to meaning "the model judged an emergency", so the pager is trustworthy again. Enterprise customers would still get a faster answer than everyone else.

**Options**, in the order I'd recommend:

1. **Cap the enterprise bump at `high`.** Enterprise raises urgency one level but never into `urgent`. The invoice copy becomes `high` (8h), ahead of ordinary `normal` (24h). A real enterprise outage still reaches `urgent`, because the model itself rates it so.
   - The gap is that an enterprise `high` and an ordinary `high` look identical and get the same deadline. The contract promise is then kept only for tickets below `high`.
2. **Option 1, plus a separate enterprise deadline.** Add a distinct hour value for enterprise tickets, for example a 4h target at `high`. This keeps the promise visibly faster at every level without touching the pager. It needs you to supply the contractual numbers, and it changes the output shape and the hour table.
3. **Leave urgency alone and add a separate `priority` or `enterprise` flag.** The agents' list sorts and badges on it. This is the least invasive for code, but the bump would still page, so it only works if paging is moved off `urgency` as well.

I suggest option 2 if your contracts name specific hours, otherwise option 1. If you pick one, tell me which and I'll implement it in `seam.py`, `test.py` and the README. Updating the charter stays with you. I'd also check the new rule against the invoice and checkout examples with unit tests, which cost nothing. No paid model run is needed for this change.