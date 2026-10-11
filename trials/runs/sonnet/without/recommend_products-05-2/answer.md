Reasons are no longer cut mid-word. The 80-character space is unchanged, and all 16 tests pass.

**Cause:** the model wasn't told about the 80-character limit, so it wrote longer sentences. `seam.py` then chopped them at character 80.

**Fix in `seam.py`:**
1. **Prompt:** it now asks for one complete sentence of at most 80 characters per reason.
2. **Rewrite:** if a reason still comes back too long, the model is asked once to rewrite only those reasons as complete sentences within the limit.
3. **Fallback:** if a rewrite is still too long or missing, the reason becomes its first complete sentence that fits. If it has no such sentence, the reason is empty. A blank line under a product looks better than a broken sentence, and the product still shows.

Every reason shown is now either a full sentence or empty, never cut off.

**Costs and caveats:**
- A search takes a second model call only when at least one reason is too long.
- The empty-reason fallback is a judgment call. If you'd rather hide the product or show a generic line, that's a small change.

**Also changed:** I replaced the old test that expected hard truncation to exactly 80 characters, added tests for the rewrite and fallback paths, and updated the README.