Recommendations now respect a price the shopper states, and all 16 tests pass.

**What changed**
- `seam.py` reads the query for a price limit and drops any model pick outside it, before the `limit` cap. If nothing is within the limit, the strip is empty, with no fallback list.
- It handles `under` / `below` / `less than` (exclusive), `max` / `maximum` / `up to` / `at most` (inclusive), `over` / `above` / `more than` (exclusive), `from` / `at least` / `min` (inclusive), and `between X and Y`.
- It accepts `€30`, `30 euro`, `30 eur`, and decimals like `19,90` or `19.90`.
- A search with no price behaves exactly as before.
- `test.py` has new tests for each phrasing, the empty-strip case, and the unfiltered catalogue.

**Where I stopped short of the charter**
The price check runs on the model's picks, not on the catalogue before the call. The charter forbids narrowing the catalogue before the model sees it, so the model still sees every in-stock product. The cost is that if the model fills its picks with out-of-range products, you can get fewer than `limit` results even when more in-range products exist.

Making the filter run before the call would fix that but moves a charter line, so that decision is yours.

**Things you might not expect**
- A query like `2 m cable` is not read as a price, but `from 100` is read as "at least 100" as you asked, so something like `from 2 m` would be misread as a price.
- During the edit, bash blocked one command and I rewrote `seam.py` in full with the Write tool instead. The final content is what the tests ran against.