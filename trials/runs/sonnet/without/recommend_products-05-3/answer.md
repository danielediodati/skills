Reasons in the strip are now never cut mid-word or mid-sentence, and the 80-character limit is unchanged. All 16 tests pass.

**Cause:** `seam.py` asked the model for a "short reason" without giving a length, then chopped whatever came back at 80 characters (`[:MAX_REASON_CHARS]`).

**Fix in `seam.py`:**
1. **Prompt:** the model is now told each reason must be one complete sentence of at most 80 characters, so most reasons arrive the right length.
2. **Leading sentences:** if a reason is still too long but its first sentence(s) fit, those are used as they are.
3. **Rewrite:** if nothing complete fits, the model is asked once, for all affected products together, to rewrite those reasons as a single sentence of at most 80 characters.
4. **Last resort:** if the rewrite is still too long, or the model drops that product, the reason is left empty. The existing "no reason" case already covers that, and an empty line seemed better than a broken sentence.

**Behaviours to check:**
- When a reason is too long and has no short leading sentence, there is a second model call. Typical searches shouldn't hit it often now that the prompt states the limit, but it is extra latency and cost on those requests.
- A shopper may occasionally see a product with no reason line. If you would prefer a fixed fallback such as the product name, that is a one-line change.

I replaced the old "capped at 80 characters" test with tests for these paths and updated the README line describing `reason`.