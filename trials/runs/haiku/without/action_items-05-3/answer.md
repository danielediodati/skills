The list no longer drops items. Every action item the model returns now comes back, and the lines the parser can't read are logged instead of vanishing. All 18 tests pass.

**What was wrong:** `extract_action_items` in `seam.py` returned only the first 10 items after sorting. The sort puts undated items last, so the cap removed exactly the follow-ups nobody had dated, like "Renew the venue contract". Nothing signalled the cut.

**What I changed:**
- **`seam.py`:** removed the `MAX_ITEMS` cap and the slice that enforced it. Lines that aren't `task | owner | due` are now logged as warnings with their text, so you can see what was skipped. Duplicate merges are logged at INFO. A `NONE` answer is not logged as a skipped line.
- **`test.py`:** replaced the cap test with one that checks 14 items all come back, with the dated item first and the undated ones after it in the model's order. Added a test that skipped lines are logged.
- **`README.md`:** changed "at most 10" to describe the new behaviour and where the logged skips appear.

**What this does not cover:** the code can only keep what the model writes. If the model never lists an item, nothing in this code can recover it, and the tool would still send a shorter list with no sign of the gap. Closing that gap needs a check against the notes, such as a second model pass that asks for any agreed actions missing from the first list, or a count comparison by the person taking notes. I haven't built either; tell me if you want one.

This folder is not a git repository, so I didn't commit anything. One command was blocked by a permission prompt, so I ran the same check with the search tool instead.