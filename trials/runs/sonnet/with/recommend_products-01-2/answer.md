Recommendations now respect a price limit stated in the search, but I couldn't run the tests. The shell was blocked partway through (a permission prompt with nobody to answer it), so the final `seam.py` has never been executed. Please run `python -m unittest` from the project directory.

**What changed**
- **`seam.py`**:
  - The search is parsed for a price limit. Supported forms:
    - upper bounds: `under`, `below`, `less than`, `cheaper than` (strict) and `max`, `maximum`, `up to`, `at most`, `no more than`, `within` (inclusive)
    - lower bounds: `over`, `above`, `more than` (strict) and `from`, `min`, `minimum`, `at least` (inclusive)
    - ranges: `between X and Y` and `from X to Y`
    - `€`/`$`/`£`, `euro` and `29,90`-style decimals are handled.
  - After the model answers, any pick outside the limit is dropped. If nothing is left, the strip is empty, with no fallback.
  - When a limit is present, the prompt also tells the model, so it doesn't waste picks on out-of-range products.
- **`evals/recommend_products/charter.md`**: added the price limit as a constrained decision, in the same change.
- **`test.py`**: added tests for each phrasing, ranges, the empty result, the prompt note, and that a search without a price behaves as before.

**Decisions to confirm**
- I did not filter the catalogue before the call. The charter forbids narrowing what the model sees, so the limit is enforced on the output instead. The catch is that a model that picks several out-of-range products can leave fewer than `limit` results. The prompt note is there to reduce that.
- Strict versus inclusive: `under 50` excludes a 50.00 product, while `max 50` and `up to 50` include it. Say if you want `under` to include the boundary.