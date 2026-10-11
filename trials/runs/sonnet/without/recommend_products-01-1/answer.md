Recommendations now respect a price limit stated in the search, and all 22 tests pass (10 of them new).

**What changed**
- **`seam.py`**: the query is parsed for price limits, and products outside them are removed from the catalogue before the model sees it. A model pick outside the limit is also dropped, since picks must come from the filtered set.
- **`test.py`**: new tests for each phrasing, the ranges, the empty case, and a search with no price.
- **`README.md`**: documents the new behaviour.

**Phrasings handled**
- **Upper limits:** `under`, `below`, `less than`, `cheaper than`, `max`, `maximum`, `up to`, `at most`, `no more than`.
- **Lower limits:** `over`, `above`, `more than`, `from`, `min`, `minimum`, `at least`.
- **Ranges:** `between 20 and 40` and `from 20 to 40`, in either order.
- **Currency:** `€30`, `30€`, `30 euro/eur`, `$` and `£`. A decimal comma (`9,5`) and thousands separators (`1.000`) also work.
- **Bounds:** `under`, `below`, `less than`, `over`, `above` and `more than` are strict, so `under 50` excludes a product at exactly 50.00. `max`, `up to`, `from` and the other phrasings are inclusive.

**Behaviour to know about**
- **Empty strip:** if nothing in stock is within the limit, the result is `[]` and the model isn't called.
- **Sizes ignored:** a number followed by a unit (`under 2 m`, `max 500 gb`) is not treated as a price, so `usb-c cable under 2 m` is unaffected.
- **No price, no change:** a search with no price behaves as before.
- **Currency is ignored:** `€`, `$` and `£` are accepted but the catalogue has no currency, so `under $30` compares against the same prices as `under 30`.
- **Limits combine:** several limits in one query are all applied.
- **Not covered:** forms like `20-40 euro` and `around 50` aren't recognised, so they're treated as having no price.