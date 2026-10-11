The strip now fills up: if the model picks fewer than `limit` products, the remaining slots go to the best-rated in-stock products not already in the strip. All 17 tests pass.

**Changes in `seam.py`**
- **Fillers:** they are sorted by rating, highest first, and ties keep catalogue order.
- **Telling them apart:** every returned product now has a `filler` field, `False` for real recommendations and `True` for fillers. Fillers also have an empty `reason`, so you can show "You may also like" with no reason line.
- **Order:** the model's picks always come first, in the order they come in today.
- **Empty strips:** a useless model answer (chatter, invented IDs, out-of-stock IDs) now gives a strip made entirely of fillers instead of an empty row.

Other changes:
- **README:** updated to describe `filler` and the top-up behaviour.
- **Tests:** four new tests cover top-up, an all-filler answer, the limit, and no fillers when the picks already fill the strip.
- **Existing tests:** five tests that implicitly relied on short results now pass an explicit `limit`. The exact-dict test also expects the new `filler` field.

**Still empty by design**
- A blank search still returns an empty list without calling the model, as before. If you want the strip filled with top-rated products even for a blank search, that's a one-line change, so tell me.
- A catalogue with nothing in stock still returns an empty list.

**Check on your side**
Anything that consumes the result now sees the extra `filler` key on each product. If something compares these dicts for exact equality, it will need updating.