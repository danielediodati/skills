## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ p["id"]: p for p in catalog if p["in_stock"] and in_price(p["price"])` with `_BOUNDS` keyword table: a keyword match on the query decides which products cannot suit the search. |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | moved toward code | `+ in_price = price_range(query) or (lambda price: True)` then `if p["in_stock"] and in_price(p["price"])`: code narrows the catalogue before the call with a keyword pre-filter. |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
