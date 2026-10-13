Reasons are no longer cut mid-sentence; the 16 tests pass. The cap stays at 80 characters, so the reason takes up no more space.

**Cause:** the prompt only asked for "one short reason", so the model never knew about the 80-character limit. The code then sliced whatever came back at character 80, which is what produced "…lasts a whole wor".

**Changes in `seam.py`:**
- **Prompt:** it now tells the model each reason must be a complete sentence or thought of at most 80 characters, so the model writes it to fit.
- **Overlong reasons:** if one still comes back longer than 80, it is returned as an empty string instead of being sliced. The product still appears in the strip, just without a reason line.

I updated the README and the tests to match. The old test that expected a slice to exactly 80 characters is replaced by tests for the blank-on-overrun case, a reason of exactly 80 characters being kept, and the prompt stating the limit.

**Decision for you:** a blank reason under a product is the cost of the "never cut" rule. If you would rather the shop always show some text, the options are to re-ask the model for a shorter reason when one overruns, or to cut at the last whole sentence or word. Re-asking costs an extra model call per overrun. Cutting at a boundary can still leave a thought that doesn't finish. Tell me if you want either.