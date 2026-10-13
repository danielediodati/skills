Every product in the strip now comes with a readable reason, and all 16 tests pass.

**Cause:** `recommend_products` in `seam.py` accepted any product the model named, even when the model left out the reason. It then returned an empty `reason`. That produced the blank gap under the Pico earbuds and the 2 m cable.

**Change in `seam.py`:**
- **Retry:** if a pick is missing its reason, the model is asked once more for just those products. That follow-up prompt asks why each one is worth the shopper's attention for this search, so it should explain the wired earbuds rather than repeat the original pick.
- **Drop:** a product that still has no reason after the retry is left out, and the next pick takes its place. The strip can therefore be shorter, but it never has a card with a hole in it.
- **No placeholder text:** I deliberately did not add a generic fallback like "Matches your search". It would fill the gap but say nothing, which is the same as having no reason.

**Tests and docs:** `test.py` no longer has the test that expected an empty reason to be returned. It now has tests for the retry, for dropping a product that still has no reason, for the next pick replacing a dropped one, and for every returned product having a reason. I also added a sentence about this to `README.md`.

**Behaviour change:** when the model omits a reason, the function now makes a second model call. If you would rather skip the retry and drop reasonless products immediately, that is a small change.