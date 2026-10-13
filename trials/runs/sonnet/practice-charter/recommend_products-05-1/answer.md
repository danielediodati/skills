I made the part of this fix that I can, and it doesn't fully guarantee what you asked for.

**Cause:** the prompt asked the model for "one short reason" but never told it the 80-character limit. The model wrote longer sentences, and `seam.py` cut them at exactly 80 characters, mid-word.

**Change:**
- `seam.py`: the prompt now tells the model each reason must be a complete sentence of at most 80 characters, so it fits the space under the product without being cut off. The number comes from `MAX_REASON_CHARS`, so the space doesn't grow.
- `test.py`: added a test that the limit reaches the prompt. All 14 tests pass.

**What this doesn't give you:** a guarantee. A model told the limit will usually write within it, but nothing in code enforces that. If one reason still runs over, it is cut mid-word as before.

**The line I haven't moved:** the charter (`evals/recommend_products/charter.md`, "Reason length and shape") says the cut at 80 characters is deliberately mid-word with no ellipsis. Making every reason read as complete would mean changing that rule in code. Options would be to cut at the last word or sentence boundary, drop or blank an over-long reason, or re-ask the model once. Each of those changes a constrained decision (the re-ask would also break the "one call, no retries" budget), so that call is yours. Cutting at a word boundary would stop the mid-word breaks but could still leave a sentence unfinished, as in your Pico example.

If the prompt change doesn't remove the cut-off reasons in practice, tell me which option you want and I'll apply it. The charter would need updating first.