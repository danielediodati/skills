## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ pick only products whose price is within it`: a rule in the prompt that fixes which products are excluded; the model can no longer judge an out-of-range product as suiting the search. |
| F2 | held | not touched |
| F3 | moved toward code | `+ and pick none if no product is.`: the prompt dictates a count of zero in that case, where the line leaves "from none to `limit`" to the model. |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | not touched: the product list sent to the model is still every in-stock product; no filtering before the call. |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched: no fallback list added; an empty answer still gives an empty strip. |
| C5 | held | not touched |
| C6 | held | not touched: still one `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
