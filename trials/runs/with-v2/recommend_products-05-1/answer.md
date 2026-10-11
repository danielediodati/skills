I changed the prompt so the model now knows its reason is capped at 80 characters, but this reduces mid-word cuts rather than guaranteeing none. The tests pass, including a new one that checks the limit reaches the model.

**Cause:** the prompt only asked for "one short reason". The model wrote natural-length sentences, and the code then cut them at 80 characters.

**Change:** in `seam.py` the prompt now says the reason is shown on one line of at most 80 characters, is cut off after that, and should be a complete thought that fits. The 80 is taken from `MAX_REASON_CHARS`, so the space under the product stays the same.

**What this doesn't guarantee:** the model can still overshoot occasionally, and the charter fixes the cut at 80 characters as a code constraint, so overshoots will still be cut mid-word. Making that fully reliable would mean moving a line the charter holds, and only you can decide that. The options are:
- **Trim to the last whole word or sentence:** this changes "cut to 80 characters". It would give no mid-word stops, but the thought could still be incomplete, as with your Pico example.
- **Drop or replace over-long reasons:** this changes "an empty reason is kept". The shopper would see no reason, or a model rewrite would cost a second call, which the charter's one-call, no-retry rule currently forbids.

Let me know if you want either option, and I'll leave the charter edit to you.