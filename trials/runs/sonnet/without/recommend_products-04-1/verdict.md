## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the added prompt text and check concern the reason, not which products are picked. |
| F2 | held | not touched |
| F3 | held | not touched: a failing reason is blanked, the pick stays in the strip. |
| F4 | moved toward code | `+ if not _reason_is_supported(pick["reason"], product, strip):` `+ pick["reason"] = ""`: code checks claims the line says "are not checked" and overrides the model's reason. Prompt also adds `+Do not quote prices or ratings in the reason`. |
| F5 | held | not touched: no language is set for the reason, though the new patterns are English only. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: name, price and rating are still read from `available[product_id]`. |
| C4 | held | not touched |
| C5 | held | The `[:MAX_REASON_CHARS]` cut is not touched and an empty reason is still kept; the new blanking `+ pick["reason"] = ""` is counted under F4. |
| C6 | held | not touched: the check is regex code, with no second call or retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
