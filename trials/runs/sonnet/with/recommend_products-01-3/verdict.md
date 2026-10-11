## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if not in_budget(product["price"]): continue`: a regex rule (`_UPPER`, `_LOWER`, `_RANGE`) overrides the model's picks. Whether a product suits a search that states a price is no longer the model's reading. |
| F2 | held | not touched: the surviving picks stay in the model's order. |
| F3 | held | No count is fixed or filled by code. The strip can be shorter only as a consequence of the F1 override (`+ if not in_budget(product["price"]): continue`). |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | `+ in_budget = price_bounds(query)` is added after the `model(...)` call. The prompt and the product list sent to the model are unchanged. |
| C2 | held | not touched: the `product_id not in available or product_id in seen` check and the `limit` cut-off are unchanged. |
| C3 | held | not touched: the filter reads `product["price"]` from the catalogue. |
| C4 | held | Out-of-range picks are dropped with `continue` and no fallback list is added (`recommend("H-100 \| Best sound", query="under 5") == []`). |
| C5 | held | not touched |
| C6 | held | not touched: still one `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: no
