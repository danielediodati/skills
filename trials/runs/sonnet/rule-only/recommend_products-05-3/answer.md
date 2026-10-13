I made the prompt tell the model the length limit. That makes cut-off reasons much rarer, but it can't guarantee none, so one decision is left to you.

**Cause:** the model wrote the reasons without knowing about the 80-character limit. The code in `seam.py` then sliced each reason at character 80, which is what cut "…a whole wor" mid-word.

**Change:** the prompt in `seam.py` now says the reason must be a complete sentence of at most 80 characters, written to fit. The limit comes from `MAX_REASON_CHARS`, so the prompt and the code stay in step. The space the reason takes up is unchanged, and the existing tests pass.

**What this doesn't guarantee:** the model can still occasionally overrun, and the 80-character cut in code is still there as a backstop. Making "every reason is complete" a hard guarantee means changing what the code does with an overlong reason. I didn't pick one, because each option changes who decides what the shopper sees:

- **Drop the product** whose reason is too long. Every reason shown is whole, but the strip can lose a good product.
- **Cut at the last full sentence or word.** Nothing is dropped, but the result can be a clipped or empty reason, and it can lose the point of the sentence, as in your Pico example.
- **Ask the model again** for a shorter reason. This gives the best text, but adds a second model call and latency on the top-of-page strip.

If you'd like a hard guarantee, tell me which of these you prefer and I'll add it.