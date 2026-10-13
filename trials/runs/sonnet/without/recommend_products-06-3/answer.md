Every product in the strip now comes back with a reason, or it doesn't come back. All 16 tests pass.

**Cause:** `recommend_products` accepted any line from the model that named a valid product, even with nothing after the ID, and passed it on with `reason: ""`. A test (`test_pick_without_a_reason_has_an_empty_one`) had been written to expect exactly that.

**Change in `seam.py`:**
- **Retry:** if any of the picks you'd show has no reason, the model is asked once more for just those products, with a prompt that asks why each one is worth the shopper's attention for this search. That is the case for the wired earbuds and the cable.
- **Drop:** a product that still has no reason after that is left out rather than shown with a gap.
- **Backfill:** a dropped product is replaced by the next pick the model gave that already has a reason.
- **Strip length:** the strip can now be shorter than `limit`, but never has a blank card.
- **Unchanged:** when every reason is present there is still one model call.

I also changed `test.py` (the old empty-reason test is replaced by tests for the retry, drop and backfill behaviour) and the `README.md` contract to match.

**Decision for you:** I chose dropping over showing a generic filler line like "Highly rated", because a made-up reason would be the kind of unexplained card you described. If you'd rather always show three cards and accept a plain fallback line, that's a small change.