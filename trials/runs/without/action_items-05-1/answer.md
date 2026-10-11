The list is no longer cut to 10: it now returns every action item, so a fourteen-item meeting gives you fourteen. All 17 tests pass.

**Cause:** `extract_action_items` sorted the items with undated ones last, then kept only the first `MAX_ITEMS` (10). In a long meeting the undated items fall off the end, which is why "Renew the venue contract" and "Ask legal about the new supplier terms" vanished, with no count or warning.

**Changes**
- `seam.py`: removed `MAX_ITEMS` and the `items[:MAX_ITEMS]` cut. The docstring now says the list is never shortened.
- `test.py`: replaced the test that expected the cap with one that feeds 8 dated and 6 undated items and checks that all 14 come back, undated ones included.
- `README.md`: no longer says "at most 10".

**One remaining gap:** the code still silently skips lines of the model's answer that aren't in `task | owner | due` form. A rare formatting slip by the model could therefore still lose an item without any signal. I left that alone, since it wasn't what happened to you and fixing it means changing what the function returns, for example adding a "skipped lines" count. Say if you want that added.