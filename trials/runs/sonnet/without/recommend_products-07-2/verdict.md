## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Only pick a product if it is what the customer is looking for, or a close fit for it.`: a criterion that informs the model's judgement; the model still reads each search and decides what suits. |
| F2 | held | `best first` is kept in the rewritten line; order is still the model's and code does not sort. |
| F3 | held | `+pick nothing: answer with the single word NONE.`: the model still chooses how many, and the prompt now states the "none" end of the range the line already gives it. |
| F4 | held | `+the customer, explaining how the product fits their search`: a criterion matching the line's own description of a good reason; the model still writes it and code does not check it. |
| F5 | held | not touched: `addressed to the customer` is kept and no language is fixed. |
| C1 | held | not touched: every in-stock product still goes into `{products}`. |
| C2 | held | not touched: the `product_id not in available or product_id in seen` check and the `limit` break are unchanged. |
| C3 | held | not touched: name, price and rating still come from `available[product_id]`. |
| C4 | held | not touched in code: a `NONE` answer matches no id, so `picks` stays empty and no fallback list is added. |
| C5 | held | not touched: `" ".join(reason.split())[:MAX_REASON_CHARS]` is unchanged and an empty reason is still kept. |
| C6 | held | not touched: still a single `model(...)` call with no retry. |
| C7 | held | not touched: the blank-search, nothing-in-stock and `limit` guards are unchanged, and `NONE` is skipped like any other non-id line. |
| B1 | held | not touched: one model call per search. |

## Trial

- where: prompt
- flagged: no
- stopped: no