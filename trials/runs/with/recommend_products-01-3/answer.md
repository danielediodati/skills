Price limits in the search are now enforced, and all 15 tests pass, including the new ones.

**What changed**
- `seam.py`: a new `price_bounds(query)` reads the limits out of the search. `recommend_products` drops any model pick outside them before applying `limit`.
- Limits recognised:
  - **Upper:** `under`, `below`, `less than`, `cheaper than`, `max`, `maximum`, `up to`, `at most` and `no more than`.
  - **Lower:** `over`, `above`, `more than`, `from`, `min`, `minimum` and `at least`.
  - **Ranges:** `between X and Y` and `from X to Y`.
  - **Number formats:** `€30`, `30 euro`, `30 eur` and `9,50`. Several limits in one search are combined.
- A search with no price behaves as before. If nothing in stock is within the limit, the strip is empty and there is no fallback list.
- Boundaries: `under`, `below`, `less than`, `over` and `above` are strict, so `under 50` excludes a 50.00 product. `max`, `up to` and `from` include the stated number.
- Dimensions are not treated as prices: `up to 2 m` and `5 cm` are ignored.
- `test.py`: tests cover each phrasing from your report, the no-price case, a dimension that is not a price, and the empty strip.

**Charter**
- The charter says the model sees the whole catalogue and code must not narrow it before the call. So the filter runs on the picks after the call. The model still sees every in-stock product.
- I added the price-limit rule to the charter's Constrained list in `evals/recommend_products/charter.md`, since this moves a decision from the model to code.

**Behaviour to know about**
- A search like `headphones under 50` can now show fewer than `limit` products, because the model picks without knowing the limit and its out-of-range picks are dropped. For example, if it picks five and three are too expensive, two are shown.
- If you would rather have the model fill the strip from in-budget products, the prompt would need to be told the limit. That is a change to what the model decides, so I left it for you to choose.