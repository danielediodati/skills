I found the cause in `triage_ticket` and fixed it. Enterprise tickets no longer land in `urgent` because of their tier, but they still get a faster deadline. All 12 tests pass.

**Cause:** the code raised the *urgency label* one level for enterprise customers. An invoice copy that the model rated `normal` became `high`. Anything the model rated `high` became `urgent`, which carries the 1-hour deadline and pages on-call. That is why a "Copy of August invoice" looked identical to a checkout outage.

**Change (`seam.py`):**
- `urgency` is now the model's assessment of the issue and is the same for every tier. `urgent` means an emergency again.
- Enterprise customers get the deadline of the next level up through `respond_within_hours`, not through the label. The promise of a faster answer is kept.

| Model says | Pro/Free | Enterprise (before) | Enterprise (now) |
|---|---|---|---|
| low | low, 72h | normal, 24h | low, **24h** |
| normal | normal, 24h | high, 8h | normal, **8h** |
| high | high, 8h | urgent, 1h, pages | high, **1h**, no page |
| urgent | urgent, 1h | urgent, 1h | urgent, 1h |

So the invoice copy is now `normal` with an 8-hour deadline. It sits ahead of ordinary tickets without showing up in the urgent list or paging anyone.

**Things to check on your side:**
- **Enterprise "high" gets a 1-hour deadline but is not `urgent`.** It matches what the old code promised in time. If your ticket list or on-call tooling pages on `respond_within_hours == 1` rather than on `urgency == "urgent"`, those tickets will still page. Page on the label.
- **Sort order.** To get enterprise tickets ahead of same-urgency tickets from other tiers, sort the agent list by urgency first and `respond_within_hours` second.
- **Contract wording.** I assumed "faster" means one level up, as the old code did. If your contracts specify actual hours, such as 4h for high, change the mapping to those numbers.
- **Tickets already marked urgent.** This only changes new tickets. Existing ones stay as they are.

I also updated the README and replaced the old enterprise test with two that cover the new behavior, including that `high` is not promoted to `urgent`.