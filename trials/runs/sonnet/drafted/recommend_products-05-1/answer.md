I haven't changed anything, because every fix for this moves a line in the `recommend_products` charter, and only you can do that.

**Cause:** The prompt asks for "one short reason" but never mentions the 80-character limit. The model writes a full sentence, and `seam.py:56` hard-cuts it at 80 characters without regard to words. Both of your examples are longer than 80 characters.

**The lines in the way** (`evals/recommend_products/charter.md`, Constrained):
- **Prompt wording:** "Prompt shape is fixed: … the instruction wording and answer format." Telling the model about the limit changes that wording.
- **Hard cut:** "hard-cut to 80 characters, no ellipsis." Cutting at a word boundary or adding an ellipsis changes that rule. It still wouldn't make the reason a complete thought, so it only hides the break.
- **Retry:** "One model call per request … No retries." Re-asking when a reason is too long would break that budget.

**What I recommend:** Add the limit to the instruction wording, for example "a reason of at most 80 characters, a complete sentence". Keep the hard cut as a backstop and keep the 80 as it is, so the space doesn't grow. The model still writes the reasons in its own words, so the free decisions stay free. This is the only option that fixes the cause. It makes truncation rare rather than impossible, because nothing in code guarantees a complete thought.

If you need a guarantee, the only way is a retry or re-ask for over-long reasons. That means a second paid call in some requests, and the charter's budget would have to change.

Do you want me to go ahead with the prompt wording change? That is a change to the charter's "instruction wording" line, which you would need to approve. If you'd rather have the guarantee, tell me and I'll work out the retry option. I won't make any paid model calls without agreeing a budget with you first.