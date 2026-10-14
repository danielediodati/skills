## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ genuinely suit the search ... Only pick a product if it is what the customer is looking for, or clearly meets the need`: criteria that inform the model's judgement, not an answer it must give. |
| F2 | held | not touched; still "best first" and the model's order. |
| F3 | held | `+ answer with exactly NONE and nothing else`: the model can now choose none; the count stays the model's, from none to `limit`. |
| F4 | held | not touched; the prompt still asks for "one short reason, addressed to the customer". |
| F5 | held | not touched; the reason is still addressed to the customer. |
| C1 | held | not touched; the full in-stock list is still sent to the model. |
| C2 | held | not touched; the `available`/`seen`/`limit` filtering is unchanged, and `NONE` is not a valid id so it is skipped. |
| C3 | held | not touched; name, price and rating still come from `available[product_id]`. |
| C4 | held | not touched; no valid pick still returns `[]` with no fallback, and `NONE` yields `[]` through the existing parse. |
| C5 | held | not touched; the `[:MAX_REASON_CHARS]` cut and the empty-reason handling are unchanged. |
| C6 | held | not touched; still a single `model(...)` call with no retry. |
| C7 | held | not touched; the blank, no-stock and `limit < 1` handling and the list-marker skipping are unchanged. |
| B1 | held | not touched; one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: no