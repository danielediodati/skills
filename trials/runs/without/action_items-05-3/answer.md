The list is no longer shortened: `extract_action_items` now returns every item the model found, including the undated ones. I haven't run it against your planting-day notes, but the tests pass.

**Cause:** the code kept only the first 10 items (`MAX_ITEMS = 10`) after sorting. Dated items sort first and undated items last, so with 14 follow-ups the four undated ones, such as the venue contract and the legal question, were the ones cut. Nothing recorded that anything had been dropped.

**Changes**
- `seam.py`: removed `MAX_ITEMS` and the slice that applied it.
- `test.py`: replaced the cap test with one that checks 15 items come back, undated ones included, with the dated one still first.
- `README.md`: no longer says "at most 10".

**What can still lose items silently:** if the model writes a line not in the `task | owner | due` form, it is skipped without any note, which could also drop a follow-up. I left that alone because it's a separate change. Reporting the skipped lines, or a count of items found versus kept, would let you spot a shortfall. Do you want me to add that?