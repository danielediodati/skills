The cause is the cap of 10 in `seam.py`. Undated items sort last, so when a meeting produces more than 10 valid items, the undated ones are the ones cut, with no sign that anything was lost. That matches your planning day: fourteen items, ten shown, and the four missing were all undated.

I haven't made the list complete, because that means raising the cap. The charter lists the cap as a constrained line and calls raising it a product decision. So that's yours to make.

What I changed:
- **`seam.py`**: added `extract_with_overflow(notes, attendees, meeting_date, model)`, which returns `(items, overflow)`. `overflow` is the number of valid items cut past the cap. `extract_action_items` is unchanged and still returns the same list. The cap is still 10.
- **`test.py`**: two tests for the overflow count. One checks that 14 valid items give 10 shown and an overflow of 4. The other checks that the overflow is 0 when everything fits. All 19 tests pass.
- **`README.md`**: a short note on the cap and the new function.

I didn't return the cut items themselves, because that would give callers a way around the cap. Because of that, you get the count but not the names. To recover them, you'd raise the cap or read the notes again.

Decision for you: if your planning days regularly exceed 10 items, the cap needs raising. Doing that is a change to the charter and the README contract, which I can't make. Tell me the number you want and I'll draft the charter change for you to approve. Nothing paid ran, so no budget was used.