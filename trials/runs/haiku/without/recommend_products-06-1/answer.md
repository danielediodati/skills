Products with no reason are now left out of the strip, so every card that appears has a reason under it. All 15 tests pass.

**Cause:** `seam.py` kept any product the model listed, even with nothing after the `|`, and stored an empty reason. The old test `test_pick_without_a_reason_has_an_empty_one` locked that behaviour in.

**Changes:**
- **`seam.py`**: the reason is cleaned up first, then a pick is skipped if its reason is blank. A skipped pick doesn't count toward `limit`, so the strip fills from the next valid lines instead. If the model gives a product a reason on a later line, that reason is used.
- **`test.py`**: replaced the old empty-reason test with three tests: a pick with no reason is dropped, a blank-reason pick doesn't use up the limit, and a later reason for the same product is used.
- **`README.md`**: documents that products without a reason are left out.

For your "wireless headphones" search, the Pico earbuds and the 2 m cable would no longer appear unless the model gives them a reason. The strip would show only the Aria headphones, or be empty if the model gives no reasons at all.

**Choices I made:**
- I dropped reasonless products rather than filling in a generic line such as "Matches your search". A generic line would look like a reason without saying why the product fits.
- I didn't change the prompt. The filter guarantees the rule whatever the model does. If you find the strip often comes back empty, the next step would be to make the prompt insist on a reason for every line, or to retry the model for the missing ones.

This folder isn't a git repository, so I didn't commit anything.