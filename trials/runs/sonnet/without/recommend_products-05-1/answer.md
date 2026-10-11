Reasons are no longer cut mid-word. A reason that doesn't fit the 80 characters is either rewritten by the model or shortened to a whole sentence or clause. All 15 tests pass.

The cause was that `seam.py` sliced each reason to 80 characters with `[:80]`, wherever that landed.

**What changed in `seam.py`**
- **Prompt:** the model is now told each reason must be a complete sentence of at most 80 characters. The 80-character limit is unchanged, so the space doesn't grow.
- **Rewrite:** if any reason still comes back too long, one extra model call asks it to rewrite just those reasons to fit while keeping the main point. Only results of 80 characters or fewer are accepted. This extra call only happens when needed, so most searches still make one call.
- **Fallback:** if the rewrite is also too long or missing, the reason becomes the longest whole sentence that fits. Failing that, it is the longest clause ending at a comma, semicolon or colon.
- **Empty reason:** if nothing fits at all, the reason is empty rather than a broken fragment.

**Tests (`test.py`)**
- I replaced `test_reason_is_one_line_and_capped`, which asserted the hard 80-character cut, with a one-line check.
- I added tests for the rewrite path and for the sentence-or-nothing fallback.

**Judgement call:** I preferred an empty reason over a clipped one. If you'd rather always show something, such as the product name, that's a small change in `_shorten_locally`.

I haven't run this against the real model, so how often the rewrite call fires in production is untested.