Enterprise tickets now get a shorter response deadline without being marked urgent, so they no longer page on-call. The unit tests pass (15 of 15), but I haven't checked how the real model labels tickets.

**What was wrong:** `seam.py` raised every enterprise ticket one urgency level. An enterprise "normal" became "high", and an enterprise "high" became "urgent", which carries the one-hour deadline and the page. The Copy of August invoice request is an example of this.

**What I changed in `seam.py`:**
- Urgency is now only what the model judges about the problem. The tier no longer changes it.
- The tier selects the deadline table. Enterprise gets 24h for `low`, 8h for `normal` and `high`, and 1h for `urgent`. Other tiers keep the existing 72/24/8/1.
- The prompt now defines the four levels. `urgent` is "something is broken for the customer right now and they cannot work". The old prompt listed the levels without defining them, which is probably part of why the model sent so much to urgent.

**Effect on your two tickets:**
- The invoice copy would now be `normal` with an 8-hour deadline. That is ahead of ordinary tickets, and it does not page.
- The checkout outage should be `urgent` with a 1-hour deadline, and it should page. That depends on the model applying the new definition, which I haven't tested.

**Choices you may want to change:**
- Enterprise `high` and `normal` share the 8-hour window. If you want `high` tighter, change the table in `seam.py`.
- Enterprise `low` moved from 24h to 24h, with the table keeping the previous behaviour for `low`. I kept it as is.

**Files changed:** `seam.py`, `test.py` (replaced the one-level-bump tests and added tests for the new behaviour), and `README.md` (updated the description of urgency and deadlines).

**Not verified:**
- I haven't run the new prompt against real tickets. Take a sample of last month's urgent list and check how many are still labelled urgent after the change.
- My test run was `python -m unittest`. My first attempt, which chained an `echo` onto it, was denied by the permission system, so I ran the command without it.
- If your helpdesk system sets its own SLA or paging rules, they sit outside this module and need the same change.