I've made the part of the fix I can, but it can't guarantee that every reason reads as complete. The tests pass, but that doesn't show the model's wording has improved.

**Cause:** the prompt only asked for "one short reason", so the model never knew about the 80-character display limit. It wrote natural sentences of any length, and the code then hard-cut them.

**Change (`seam.py`):** the prompt now says the reason is shown in a fixed space, that anything beyond 80 characters is cut off, and that it should be a complete sentence within 80 characters. The limit is read from `MAX_REASON_CHARS`, so the two can't drift apart. I added a test that the prompt states the limit. The space the reason takes up is unchanged.

**What this can't promise:** the model can still overshoot, and when it does the code still hard-cuts, mid-word if need be. Making the guarantee absolute means changing how over-long reasons are handled, and the charter (`evals/recommend_products/charter.md`) fixes that as "hard-cut at 80, no ellipsis, may cut mid-word". Changing it would move a line, so I've left it alone. Any of these would need your decision:

- **Cut at the last word boundary or sentence end:** this removes mid-word breaks, but a reason can still read as unfinished (your Pico example would still lose its point).
- **Drop the reason, or the product, when it exceeds 80 characters:** the strip is always clean, but some products show without a reason or disappear.
- **Retry or re-ask the model for a shorter reason:** this gets complete thoughts, but costs a second call, and the charter fixes exactly one call per request.

I'd try the prompt change first and check real output. If cut-offs still show up, the word-boundary cut is the cheapest next step.