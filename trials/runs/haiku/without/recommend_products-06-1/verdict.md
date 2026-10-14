```
## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ or not reason` in the skip condition: code now drops picks the model made, so it fixes the count more tightly than "none to `limit`". |
| F4 | held | not touched; the reason's content is still the model's and unchecked. |
| F5 | held | not touched |
| C1 | held | not touched; the prompt and the product list sent to the model are unchanged. |
| C2 | held | not touched; the check on real, in-stock, unseen ids is intact and `if len(picks) == limit: break` is unchanged. |
| C3 | held | not touched; name, price and rating still come from `available[product_id]`. |
| C4 | held | not touched; no fallback list is added and no valid pick still gives an empty list. |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS]` / `+ or not reason`: the line says an empty reason is kept, and code now drops the product instead. |
| C6 | held | not touched; still one model call and no retry. |
| C7 | held | not touched; the blank search, empty stock and `limit` checks and the marker skipping are unchanged. |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: code
- flagged: yes
- stopped: no
```