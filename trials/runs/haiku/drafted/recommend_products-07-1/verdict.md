## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Only pick a product the customer is looking for, or a close alternative to it (a synonym, or the same need).` A criterion the model applies by reading each search; it does not fix the answer. |
| F2 | held | `best first` is kept in the new prompt line; the order is still the model's. |
| F3 | held | `+ If no product suits the search, answer with nothing`: the model still decides how many, from none to `limit`. |
| F4 | held | `+ saying how the product suits this search` guides the reason without fixing its content; claims are still unchecked. |
| F5 | held | `addressed to the customer` is kept; the language is still the model's. |
| C1 | held | not touched; the product list is still every in-stock product. |
| C2 | held | not touched; the `available` and `seen` checks and the `limit` break are unchanged. |
| C3 | held | not touched; name, price and rating still come from `available[product_id]`. |
| C4 | held | not touched; no fallback is added, and an answer with no valid ids still gives `[]`. |
| C5 | held | not touched; `" ".join(reason.split())[:MAX_REASON_CHARS]` is unchanged and an empty reason is kept. |
| C6 | held | not touched; there is still a single `model(...)` call and no retry. |
| C7 | held | not touched; the blank-search and no-stock early return, the `limit` check and the list-marker skipping are unchanged. |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: prompt
- flagged: no
- stopped: no