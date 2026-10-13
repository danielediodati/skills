The recommender can now return nothing, so a search like "kettle" should produce an empty list instead of three unrelated products. The tests pass, but I haven't run it against a real model.

**Cause:** the prompt in `seam.py` told the model to "pick up to {limit} products that best match", with no way to say "none". The model was forced to fill the strip, and it padded it with popular, cheap or highly rated items. That explains reasons like "A popular choice with our customers".

**Changes:**
- **`seam.py`:** the prompt now says to pick only products that genuinely suit the search. It tells the model not to pick on popularity, price or rating, and to answer `NONE` if nothing fits. Reasons must now explain how the product fits the search.
- **Parsing:** I left it unchanged. A `NONE` answer already parses to an empty list, because the parser skips any line that isn't a real catalogue ID.
- **`test.py`:** two new tests cover a `NONE` answer and the prompt's opt-out wording.
- **`README.md`:** documents the new behaviour.

**Still needed:** the page should hide the "Recommended for your search" strip, heading included, when the list is empty. That rendering code isn't in this repo. Otherwise shoppers will see a heading over nothing.

**Limit:** relevance is still judged by the model. The prompt change should stop the forced padding, but check a few real queries ("kettle", a misspelling, a brand you don't carry) against your actual model. If it still pads, the next step is to ask the model for a relevance score per product and drop low scores in code.