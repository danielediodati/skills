I changed the prompt so the model is told the limit. This makes complete reasons much more likely, but it does not guarantee them. The 14 local tests pass, and I made no paid model calls.

**What changed**
- **Prompt (`seam.py`):** it now says each reason is shown on one line of at most 80 characters and must be a complete thought that fits, written short enough to finish. The limit comes from `MAX_REASON_CHARS`, so the prompt and the cut stay in step.
- **Test (`test.py`):** one new test checks that the limit reaches the model.
- **Space:** the reason takes up the same space as before.

**Why it is not a guarantee**
- Today the model is never told about the 80-character limit, so it writes natural-length sentences and the code chops them. That is why you saw "whole wor".
- A model can still overshoot, and anything over 80 characters is still cut exactly as before.
- The charter fixes that cut as a hard display limit and a plain truncation, with no ellipsis, word-boundary trim or re-ask. Ending every reason cleanly would mean changing that line. I haven't, and the decision is yours.

**Options if you want a guarantee**
1. **Trim at the last word or sentence boundary.** It's free and deterministic, and it never shows a half word. It can still drop the end of the thought, as in your Pico example.
2. **Re-ask the model for a shorter reason when one is over the limit.** Reasons read as complete, but it adds a second paid call, which breaks the one-call-per-request budget.
3. **Show no reason when it doesn't fit.** The strip is always clean, but some products appear with nothing underneath.

My recommendation is to ship the prompt change and see how many reasons still overshoot. If any do, option 1 is the cheapest next step. Verifying that against a real model would need a paid run, and I'd agree a budget with you first.