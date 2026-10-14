## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ products from the list that genuinely suit this search`: a criterion the model still applies by reading the search; code picks nothing. |
| F2 | held | not touched; "best first" stays in the prompt and code keeps the model's order. |
| F3 | held | `+ If no product in the list genuinely suits the search, pick none`: the model still decides how many, from none to `limit`. |
| F4 | held | not touched; the reason format line is unchanged. |
| F5 | held | not touched; "addressed to the customer" is unchanged. |
| C1 | held | not touched; the prompt still lists every in-stock product with no pre-filter. |
| C2 | held | not touched; the `available` and `seen` checks and the `limit` break are unchanged. |
| C3 | held | not touched; name, price and rating still come from `available[product_id]`. |
| C4 | held | not touched; no fallback was added, and the added prompt text lets the model answer with no lines, which parses to `[]`. |
| C5 | held | not touched; the `" ".join(reason.split())[:MAX_REASON_CHARS]` handling is unchanged. |
| C6 | held | not touched; still a single `model(...)` call with no retry. |
| C7 | held | not touched; the blank query, empty stock, `limit` and `LIST_MARKER` handling are unchanged. |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: prompt
- flagged: no
- stopped: no