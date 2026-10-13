The cut is now detectable, and the cut items are kept. The list itself is still capped at 10, so the full set of fourteen is only partly addressed. All 20 tests pass; no paid calls were made.

**Cause:** the code sorts the items, puts undated ones last, and keeps the first 10. Your four undated items sat at the end and were dropped, and nothing recorded that anything was dropped.

**What I changed** (`seam.py`):
- Added `extract_with_overflow`, which returns an `Extraction` with `items` (the same capped list), `omitted` (the valid items the cap cut) and `complete` (`False` if anything was cut). For your planning day it would have returned 10 items, with "Renew the venue contract" and "Ask legal about the new supplier terms" among the four in `omitted`.
- `extract_action_items` behaves exactly as before.
- Added tests for the new behaviour and a README note.

**Still open:** the tool that sends the list round has to call `extract_with_overflow` and show a warning plus the omitted items when `complete` is `False`. That code isn't in this directory, so I couldn't wire it in.

**The line I did not move:** the 10-item cap is listed in the charter as a constrained decision, with extra items "silently discarded". Only you can change it. Raising it, say to 25, would put all fourteen in the list itself, which is what you asked for. The cost is a longer list to send round or load into a tracker. The charter says 10 was a readability choice and "may be raised". Tell me the number, or keep 10 and rely on the warning. Either way, the charter's "silently discarded" wording is now out of date, and I did not edit it.