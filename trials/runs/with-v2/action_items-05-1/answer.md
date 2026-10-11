I removed the cap of 10, so a long meeting now returns every item the model found. That was the cause of the lost follow-ups.

**Cause:** `extract_action_items` sorted dated items first and then kept only `items[:10]`. In a 14-item meeting, the four undated items sat at the end and were cut, with no count or note. That is why "Renew the venue contract" and "Ask legal about the new supplier terms" disappeared.

**Changes:**
- `seam.py`: dropped `MAX_ITEMS` and the slice.
- `test.py`: replaced the cap test with one that checks 15 items, undated ones included, all survive.
- `README.md`: no longer says "at most 10".
- All 17 tests pass.

The charter already says "No cap on the number of items", so this brings the code in line with it and moves no line. I did not edit the charter.

**Not covered:**
- **Rejected dates:** the charter notes a second gap in the code that I left alone. A due date the code rejects (unreadable, or before the meeting) becomes `None`, so it looks the same as "no date given". An item could therefore show as undated when the notes did give a date. It doesn't lose items, but it can mislead.
- **Model misses:** the code can no longer drop items, but it cannot catch the model failing to list one. That is a judgement the charter leaves to the model. If you want a stronger guarantee, say so, and we can discuss what a check there would look like.