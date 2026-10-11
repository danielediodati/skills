The strip now fills up to `limit` whenever enough products are in stock. The full test suite passes (17 tests).

**What changed in `seam.py`**
- The model's picks come first, in the same order as today, each with `"filler": False`.
- If there are fewer than `limit`, the remaining slots take the best-rated in-stock products not already in the strip, highest rating first.
- Ties on rating keep catalogue order.
- Each filler has `"filler": True` and `"reason": ""`, so you can show it under "You may also like" with no reason line.
- If the model returns garbage or nothing usable, the whole strip is fillers.
- If fewer than `limit` products are in stock, you get all of them.

**Things to know**
- Every returned product now has a `filler` key, so the output shape changed. I updated the existing test that compared whole dicts and the README.
- I added tests for a short answer, an unusable answer, the limit, and a small catalogue.
- A blank search still returns an empty list without calling the model, as documented. If you want the strip filled with top-rated products even for a blank search, that is a one-line change. Say if you want it.