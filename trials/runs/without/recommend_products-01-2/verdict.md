## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ available = {i: p for i, p in available.items() if within_limits(p["price"])}`: a keyword rule (`under\|below\|less\s+than...`) decides which products cannot suit the search. |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | moved toward code | `+ if within_limits:` / `+ available = {... if within_limits(p["price"])}` before the call; docstring adds "products outside it are never offered to the model": code narrows the catalogue with a keyword pre-filter. |
| C2 | held | not touched: the loop still checks `product_id not in available or product_id in seen` and stops at `limit`. |
| C3 | held | not touched |
| C4 | held | not touched: nothing within the price limit returns `[]`, with no fallback list. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched: `if not query or not available: return []` is unchanged; the new early return on an emptied `available` comes from the pre-filter counted under C1. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
