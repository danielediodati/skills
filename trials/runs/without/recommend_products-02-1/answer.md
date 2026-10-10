The strip now fills up to the limit whenever enough products are in stock, and the fillers are marked so you can label them. All 17 tests pass, including 4 new ones for the filling behaviour.

**What changed in `seam.py`**
- **Order:** the model's picks come first, in the same order as today.
- **Filling:** any remaining slots go to the best-rated in-stock products not already in the strip, highest rating first. Ties keep catalogue order.
- **Marking:** every item now has a `filler` field. It is `False` for real recommendations. It is `True` for fillers, which also have an empty `reason`, so they can sit under "You may also like" with no reason line.
- **Short lists:** the list is shorter than `limit` only when fewer than `limit` products are in stock.
- **Empty strip:** when the model returns nothing usable, the strip is now all fillers.

**Also updated**
- **Tests:** existing assertions that compared the full list now look at real picks only.
- **README:** it documents the new field and the filling rule.

**Decision for you:** a blank search still returns an empty list without calling the model, as the README documents. If you want the strip filled with top-rated products there too, it's a one-line change.