The strip now returns nothing when no product fits, instead of filling up with unrelated items. All 15 tests pass.

**The cause:** the prompt in `seam.py` told the model to "pick up to N products that best match", so it always filled the slots. Nothing in the code checked relevance, so the Aria headphones, the USB-C cable and the Pico earbuds went out under "Recommended for your search" for "kettle".

**What I changed:**
- **Prompt (`seam.py`):** the model is now told to pick only products that genuinely suit the search, or a clear alternative to it. If nothing fits, it should pick none and answer with nothing.
- **Tests (`test.py`):** I added two. One checks that the prompt carries the new instructions. The other checks that an answer with no usable picks, like "I cannot find a kettle here.", gives an empty list.

**Limits of this fix:**
- The tests use a fake model, so they confirm the parsing and the prompt wording, not how the real model judges relevance. Please try a few searches against the live model before relying on it: "kettle", a misspelling, an unstocked brand, and a search where the strip should work, such as "headphones".
- The model may still pick loose alternatives for some searches. If that happens, the next step is a relevance check in code, not more prompt wording.
- The page code isn't in this folder. The strip has to hide itself when `recommend_products` returns an empty list. If it shows a heading with nothing under it, that part needs fixing where the page is rendered.

I didn't commit anything, since this folder isn't a git repository.