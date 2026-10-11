The model is now told the limit, so it should write reasons that fit. Reasons can still be cut mid-word, because the code cut remains as a backstop. The 13 tests pass.

**Cause:** the model was never told reasons are limited to 80 characters. It wrote natural-length sentences, and the code then sliced them at 80 characters. That slicing is what produced "…lasts a whole wor".

**Change (`seam.py`):** the prompt now asks for a complete sentence of at most 80 characters, and explains that longer text is cut off. The limit comes from the existing `MAX_REASON_CHARS`, so the space under each product is unchanged.

**What this doesn't guarantee:** a model can still overshoot, and an over-long reason would be cut exactly as before. I couldn't check real model output here, so please run a few searches such as "headphones for travel" and see how often reasons now fit.

**A decision for you:** to make it fully reliable, two things would have to change in the charter:
- **Retry on overlong reasons:** call the model again when a reason is too long. The charter says one model call and no retry, because the strip sits at the top of the page.
- **Shorten at a word boundary:** cut at the last whole word and add an ellipsis. It would never break a word, but it would still drop the end of the thought, as in your Pico example.

I haven't touched either, since each moves a line that only you can change.