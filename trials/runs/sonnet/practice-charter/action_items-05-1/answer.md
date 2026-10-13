I made the cut visible, but the list itself still stops at ten. Getting all fourteen needs a decision from you, described below. All 19 tests pass.

**What went wrong**
- The model did find all fourteen items.
- Code then sorts the items by deadline, with undated ones last, and truncates at `MAX_ITEMS = 10`. That is why the undated ones, such as the venue contract and the legal question, were the ones lost.
- Nothing reported the cut, which is why the list looked complete.

**What I changed (`seam.py`, `test.py`)**
- I added `extract_action_items_with_overflow(...)`, which returns `(kept, cut)`.
  - `kept` is exactly what `extract_action_items` returns.
  - `cut` holds the items that were found but didn't fit, in the same order.
- `extract_action_items` behaves as before and now just calls it.
- For your planning day, `cut` would have held the four missing items. The tool that sends the list round needs to switch to this function, so it can show them or at least say "4 more items not shown".

**The line I did not move**
- The charter makes "at most 10 items" a code-enforced constraint.
- Raising or removing the cap is what would put all fourteen in the list itself. I can't make that change without moving the line, so it is your decision.
- Alternatively, the tool could show `cut` as a separate "not shown" section, which keeps the cap.
- I also left the prompt alone. Telling the model about the cap would make it drop items on its own, silently and before the code sees them.

I did not edit the charter or the README. The charter's "Not yet in code" note on the cap is still accurate, and the README doesn't mention the new function yet.