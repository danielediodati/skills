Cut items can no longer disappear without a sign, but the list is still capped at 10, so a 14-item meeting still returns 10 items.

**Cause.** `MAX_ITEMS = 10` in `seam.py` truncates the list after sorting. Undated items sort last, so they are the ones dropped, which matches your four missing follow-ups. Nothing reported the cut.

**What I changed (`seam.py`, `test.py`):**
- `extract_action_items` still returns at most 10 items. When it cuts any, it now raises a `UserWarning` giving the number cut and their task names, e.g. "4 action item(s) beyond the limit of 10 were left out of the list: Renew the venue contract; …".
- New `extract_with_omitted(...)` returns an `Extraction(items, omitted)`, so the notes tool can show the cut items next to the list, or print "10 of 14 shown".
- Tests added for the warning, the `omitted` list, and no warning when nothing is cut. All 19 tests pass.

**Still open: the cap of 10.** I left it alone. How many items the list may hold is a decision the code takes, and raising or removing the limit would move that line, which is yours to decide. Raising it, or removing it, would give you all fourteen in one list. Tell me which you want and I'll do it.

**Wiring needed.** I only see this module, not the notes tool that calls it. For you to see the warning or the omitted items, the tool must show them, for instance by calling `extract_with_omitted` and printing the omitted tasks under the list.