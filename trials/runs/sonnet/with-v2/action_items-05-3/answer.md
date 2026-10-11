The list no longer loses items: the fourteen in your planning day would now all come through, including the undated ones like "Renew the venue contract" and "Ask legal about the new supplier terms". All 17 tests pass.

**Cause:** `seam.py` cut the list to 10 after sorting. Undated items sort last, so they were the ones dropped, and nothing reported the cut.

**Changes:**
- **`seam.py`:** removed the `MAX_ITEMS = 10` cap.
- **`test.py`:** replaced the cap test with one that feeds 15 items and checks all 15 come back, with undated ones kept after the dated one.
- **`README.md`:** no longer says "at most 10".

The charter already said "No cap on the number of items. Not yet in code", so I only brought the code in line and did not edit the charter.

**Still open:**
- **Dropped owners and dates:** an owner who isn't an attendee, or a deadline that is rejected, is still silently set to `None`. The charter lists both as not yet in code, but fixing them means deciding how the result carries that information, so I left them for you.
- **Missed items:** the model can still miss an item in the first place. Only a count against the notes would catch that, and the charter doesn't cover one, so it's your call whether to add it.