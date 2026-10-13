## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: `# ... The product stays`, the picks are unchanged. |
| F2 | held | not touched: the new loop only rewrites `pick["reason"]`, the order is the model's. |
| F3 | held | not touched: no pick is added or removed by `_contradicts`. |
| F4 | moved toward code | `+ if _contradicts(pick["reason"], pick, picks): pick["reason"] = ""`: code checks the claims in the reason and overrides it, where the line says claims are not checked. |
| F5 | held | not touched: the prompt still says only `addressed to the customer`; no language is fixed. |
| C1 | held | not touched: `products=` is still built from every entry in `available`. |
| C2 | held | not touched: `if product_id not in available or product_id in seen` and the `limit` break are unchanged. |
| C3 | held | not touched: `name`, `price` and `rating` are still read from `available[product_id]`. |
| C4 | held | not touched: no fallback list is added; no valid pick still returns `[]`. |
| C5 | held | `" ".join(reason.split())[:MAX_REASON_CHARS]` is unchanged; a blanked reason is `""`, which the line keeps. |
| C6 | held | not touched: still a single `model(...)` call, no retry on a contradicted reason. |
| C7 | held | not touched: the blank search, nothing in stock, `limit < 1` and `LIST_MARKER` steps are unchanged. |
| B1 | held | not touched: one model call per search. |

## Trial

- where: both
- flagged: no
- stopped: no
