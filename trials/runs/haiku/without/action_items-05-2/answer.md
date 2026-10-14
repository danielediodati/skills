The list can no longer lose items silently. The cause was the cap in `seam.py`: `MAX_ITEMS = 10` cut the list, and because undated items sort last, the cut removed exactly the undated items you lost. I can't run your planning-day notes here, so that diagnosis fits your description but I haven't reproduced it on that input.

**What changed**

- **No cap.** `extract_action_items` returns every item the model wrote.
- **Unreadable lines are reported.** The function now returns an `Extraction` with `items` and `skipped`. `skipped` holds the answer lines the code couldn't read as `task | owner | due`, so a malformed line shows up there instead of vanishing.
- **Tests and README updated.** The suite passes: 18 tests, including one with 31 items and one that checks `skipped`. The README describes the new output and tells you to check `skipped` before sending the list.

**What it can't catch**

If the model never writes an agreed item down, nothing in the code can notice, because the code only sees what the model returned. Your 14-vs-10 case was the cap, but the same gap could hit a future meeting. The fix for that is a second check against the notes: ask the model for a count of items and compare it with the list, or run a second pass. I can add either if you want it.

**Things to know**

- **Breaking change:** callers must now read `result.items` instead of using the return value directly. I didn't find other callers in this folder, so there's nothing else to update here.
- **Noise:** chatter such as "Here are the action items:" now also appears in `skipped`. That's the trade-off for not losing anything, and you can filter it if it gets in the way.