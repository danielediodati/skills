Reasons are no longer cut mid-word: a reason is now either a complete sentence that fits in 80 characters or empty, and the 80-character space is unchanged. The tests pass.

**What changed in `seam.py`**
- **Prompt:** The model is now told its reason must be one complete sentence of at most 80 characters and to say less rather than run over. This is the main fix, since the model writes the wording and can now write to fit.
- **Overlong reasons:** If a reason still runs over, the code keeps the longest leading complete sentences that fit. If no sentence fits, the reason is empty, so the product shows with no line under it.

**Decision for you:** an empty reason is the one visible trade-off. I chose a blank line over a half-sentence, and the product itself still appears. The alternative is to re-ask the model to shorten the reason, which costs an extra model call per overlong reason. Say if you want that instead.

I replaced the old "capped at exactly 80 characters" test with ones covering the new behaviour, in `test.py`.