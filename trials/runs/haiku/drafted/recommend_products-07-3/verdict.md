## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ products from the list that genuinely suit the search` / `+ A product that is only loosely related... does not suit it.`: a criterion the model applies by reading each search; code decides nothing. |
| F2 | held | not touched; "best first" stays in the prompt and code keeps the model's order. |
| F3 | held | `+ If none of the products suits the search, answer with nothing.`: the model still picks how many, from none to `limit`; no count is fixed. |
| F4 | held | not touched; the reason is still written by the model. |
| F5 | held | not touched; the reason is still addressed to the customer. |
| C1 | held | not touched; the model still sees every in-stock product and there is no pre-filter. |
| C2 | held | not touched; the id, in-stock, dedup and `limit` checks in code are unchanged. |
| C3 | held | not touched; name, price and rating still come from the catalogue. |
| C4 | held | not touched; code still returns `[]` when no valid pick comes back, with no fallback added. |
| C5 | held | not touched; the reason is still cut to `MAX_REASON_CHARS` and an empty reason is kept. |
| C6 | held | not touched; still one model call and no retry. |
| C7 | held | not touched; the blank-search, nothing-in-stock, `limit < 1` and list-marker handling is unchanged. |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: prompt
- flagged: no
- stopped: no