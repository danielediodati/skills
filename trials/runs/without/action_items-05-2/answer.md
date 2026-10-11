The list is no longer shortened: all 17 tests pass, including a new one with 15 items (14 undated) that checks none are dropped.

**Cause:** `extract_action_items` sorted the items with dated ones first, then cut the list to `MAX_ITEMS = 10` with `items[:MAX_ITEMS]`. On a big meeting the undated items sit at the end of the sort, so they were the ones dropped, and nothing reported the cut. Your four missing items fit that: undated, and past item ten.

**Changes**
- `seam.py`: removed the cap, so every item the model returns comes back. The order is the same as before, dated items soonest first and undated last.
- `test.py`: replaced the "list is capped" test with one asserting a long list comes back whole, undated items included.
- `README.md`: no longer says "at most 10".

**Still possible**
- The code can still skip lines the model wrote in the wrong format, and it merges repeats of the same task and owner. Both are logged nowhere. These are much rarer than the cap, but a line malformed by the model would still vanish without notice.
- It can't catch an item the model never wrote down. If you want a safeguard there, I could have the function report how many lines it skipped, which would change the return type, so I haven't done it.