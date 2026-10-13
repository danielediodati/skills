The list can no longer be cut without saying so. All 19 tests pass, including two new ones for this.

**What was happening:** `extract_action_items` caps the list at 10, and the cap is applied after sorting. Dated items sort first, so a 14-item meeting loses its undated ones, such as the venue contract and the legal question. The function returned only the first 10 and nothing recorded the rest.

**What changed in `seam.py`:**
- The function now returns an `ActionItemList`, which is still an ordinary list of at most 10 items, so existing callers keep working.
- `.omitted` holds the items that were found but cut.
- `.truncated` is `True` when anything was cut.
- Your tool can use these to show "10 of 14 shown" and list the remaining four, or to refuse to send a list that was cut.

**What I did not change:** the cap of 10, its position after the sort, and the rule that undated items are dropped first. The charter treats these as constraints, so they stay as they were. The list you send round is still capped at 10.

**Two decisions that are yours:**
1. **Raising `MAX_ITEMS`.** The charter calls 10 a tunable budget, so raising it to something like 25 would make your planning-day case come out complete. I left it alone because the number is your call. With the new `.omitted`, a long meeting is at least flagged.
2. **The tool that calls this function.** It isn't in this directory, so nothing yet displays `.truncated`. Until it does, the warning exists in the data but not on the page you read. That wiring is the remaining step before you can trust the sent list.

I didn't touch the charter or README. Both still describe the output as "at most 10 items", which remains true of the list itself. The README doesn't mention `.omitted` yet.