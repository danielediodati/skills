The list no longer loses items: the cap of 10 is gone, so a meeting with fourteen follow-ups returns all fourteen. The 17 tests pass.

**Cause:** `extract_action_items` sorted dated items first and then kept only the first 10 (`items[:MAX_ITEMS]`). The undated items sit at the end of that order, so in a long meeting they were the ones cut, silently. That matches your four missing tasks, including "Renew the venue contract" and "Ask legal about the new supplier terms".

**Changes:**
- `seam.py`: removed `MAX_ITEMS` and the slice. The charter already says "no cap on the number of items".
- `test.py`: replaced the cap test with one that checks 15 items all come back, with undated ones last.
- `README.md`: no longer says "at most 10".

**Not changed:**
- Two other items in the charter are still marked "not yet in code". An owner who isn't an attendee becomes `None`, so their name is lost. A deadline that code rejects becomes `None`, so it looks like no deadline was given. Neither dropped your items, so I left them. Say if you want them done.
- The model can still skip an action item when it reads the notes. Code can't detect that, so the list is only as complete as the model's reading.