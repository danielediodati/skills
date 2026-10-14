The strip can now come back empty. For a search like "kettle", the model is told it may answer `NONE`, and the code then returns no products, so the page shows only the "no results" message.

**Cause:** in `seam.py`, the prompt said "Pick up to {limit} products" and offered no way to pick nothing. The model filled the slots with whatever was closest, usually the bestsellers, and the code passed those through.

**Changes:**
- **`seam.py`:** the prompt now asks for products that genuinely suit the search. It says not to pick products just for being popular, highly rated or cheap, or for sharing a word with the search. If nothing fits, the model answers exactly `NONE`. The parsing code needed no change, because `NONE` contains no valid product ID and so yields an empty list.
- **`test.py`:** two new tests. One checks that a `NONE` answer gives an empty strip. The other checks that the prompt contains the new instructions.

All 15 tests pass with `python -m unittest`.

**Not verified:** the tests use a fake model, so they cannot show how a real model answers "kettle". The prompt change makes an empty strip the expected answer, but the model can still make a poor pick. Testing against the real model with your own searches, such as "kettle", a misspelled brand and a stocked product, would confirm it.

**Choices I made:** I kept misspellings of products you do stock as matches, since those are real searches for the product. I left the "addressed to the customer" reason wording unchanged, although it may be part of why the reasons sound like generic praise. If you want the strip to be stricter still, the next step would be a code-side check that a pick's reason refers to the search.