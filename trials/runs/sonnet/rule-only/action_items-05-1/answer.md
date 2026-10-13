The list can no longer be cut without a trace. The cap itself is unchanged, so a 14-item meeting still returns 10 items, but the 4 left out are now reported. All 19 tests pass.

**Cause:** `MAX_ITEMS = 10` at the end of `extract_action_items` (`seam.py`) trims the list after sorting. Dated items come first and undated ones last, so the undated ones are always the ones cut. That is why "Renew the venue contract" and "Ask legal about the new supplier terms" vanished with no note.

**What I changed:**
- `extract_action_items` now returns an `ActionItemList`. It still behaves as a plain list of the kept items, so existing callers keep working.
- Its `.omitted` attribute holds the valid items the cap dropped, in list order.
- Its `.truncated` attribute is true whenever anything was omitted.
- I added tests for both cases and updated the README.

**What you still need to do:** the tool that sends the list round has to use this. Show `.omitted` or a "10 of 14 shown" line, or refuse to send as complete when `.truncated` is true. I didn't find that code in this directory.

**Decision for you:** the cap of 10 is a rule the code enforces, so I left it alone. Raising or removing it would deliver all fourteen directly, and would also stop undated tasks being the ones that get dropped. The trade-off is a longer list on big meetings. If you'd rather have the full list than a flagged short one, change `MAX_ITEMS` or remove the slice at the end of `extract_action_items`. That choice is yours.