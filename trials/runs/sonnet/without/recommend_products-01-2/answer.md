Searches that state a price limit now only recommend products inside it. All 19 tests pass, including the new ones.

**How it works (`seam.py`)**
- The query is parsed for a price limit before the model is called.
- Products outside the limit are removed from the list the model sees, so it can't pick them and none can come back in the strip.
- If nothing in stock is within the limit, the function returns `[]` without calling the model.
- Queries with no price in them behave exactly as before.

**Phrasings handled**
| Phrasing | Rule |
|---|---|
| `under`, `below`, `less than`, `cheaper than` | strictly below |
| `max`, `maximum`, `up to`, `at most`, `no more than` | at or below |
| `over`, `above`, `more than` | strictly above |
| `from`, `min`, `minimum`, `at least` | at or above |
| `between 20 and 40`, `from 20 to 40` | inclusive range (reversed order is fixed) |

- **Number formats:** `€`, `$` and `£` before the number and `euro`/`eur` after it are fine. Decimals like `30,50` and thousands like `1,000` also parse.
- **Combined limits:** if a query has several, all of them must hold.

**Behaviours to be aware of**
- **Strict vs. inclusive:** `under 50` excludes a product priced exactly 50.00, while `max 50` includes it. That's my reading of the wording, so say if you'd rather treat them the same.
- **Units are not prices:** a number followed by a unit, like `under 50 gb` or `max 30 w`, is ignored, so those searches get no price filter.
- **Not handled:** plain ranges like `20-40` or `20 to 40` without `between`/`from`, and currencies other than the symbols above.

The new tests are in `test.py`. I didn't update the README; the new rule probably belongs there as one sentence.