The cut is no longer silent, but the list still stops at 10, so a 14-item meeting still returns 10 items. The four undated items you lost now come back on the result as `omitted`. All 19 unit tests pass, with no model calls and nothing paid.

**Cause.** The model did find all 14. After sorting, dated items first and undated last, the code keeps only the first 10 (`seam.py`, `MAX_ITEMS`). That cap cut exactly the undated items, and nothing recorded that it had happened.

**What I changed**
- **Return type:** `extract_action_items` returns an `ActionItems`, a normal `list` subclass, so existing callers and tests behave the same.
- **New attributes:** it carries `.omitted`, the items that were found but did not fit, and `.truncated`, which is `True` when there are any.
- **Your meeting:** the result would have 10 items, `.omitted` would hold "Renew the venue contract" and "Ask legal about the new supplier terms" among the four, and `.truncated` would be `True`.
- **Tests and docs:** I added two tests for this, and the README now mentions the attributes.

**What still needs your decision**
- **The cap itself.** To get all fourteen in the list you send round, `MAX_ITEMS` has to go up or the cap has to go away. The charter lists the cap of 10 as a constraint the code owns, so raising it is your call. It would also leave the charter's "at most 10" out of date, and I don't edit the charter. Raising it to something like 25 is the smallest change that would have given you all fourteen.
- **Whoever sends the list.** The meeting-notes tool that calls this function has to show `.omitted` or a "4 more not shown" note in what it sends. That caller isn't in this repo, so I couldn't change it.

Do you want to raise or remove the cap, and if so to what?