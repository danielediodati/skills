Price limits in the search are now applied before the model sees the catalogue, but I couldn't run the final version of the tests, so it's unverified by execution.

Bash was denied partway through, after my earlier test runs had failed on a bug I then fixed in `seam.py`. I traced the new test cases by hand and they come out as expected. Please run `python -m unittest` to confirm.

**What changed**
- **`seam.py`**: a new `price_range(query)` reads the limit from the search, and `recommend_products` drops in-stock products outside it. Filtering the catalogue means the model never sees out-of-range items and can't recommend one. If nothing is left, it returns `[]` without calling the model.
- **`test.py`**: new cases for the phrasings you listed, the empty-strip case, and searches where a number isn't a price.

**What it understands**
- **Upper limits**:
  - Exclusive: `under`, `below`, `less than`, `cheaper than`, `<`.
  - Inclusive: `max`, `maximum`, `up to`, `at most`, `no more than`, `<=`.
- **Lower limits**:
  - Exclusive: `over`, `above`, `more than`, `>`.
  - Inclusive: `from`, `at least`, `min`, `>=`.
- **Ranges**: `between 20 and 40` and `from 20 to 40`.
- **Number formats**: `€30`, `$30`, `30 euro`, `29,90` and `1,000` all parse.
- **Several limits**: they combine, so `over 5 under 9` means 5 to 9.

**Behaviour to know about**
- `under 50` and `over 100` exclude the stated number itself, while `max 30`, `up to 30` and `from 100` include it.
- A number attached to letters, as in `pro max 256gb`, is not treated as a price.
- `under 50 cm` would be read as a price limit, since the code can't tell units from currency.

The README still describes the old behaviour; I haven't updated it.