## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if not _reason_agrees(pick["reason"], pick, picks): pick["reason"] = ""` and `+ The reason must not state or hint at a price, a rating...`: keyword rules override the reason, where the line says claims are not checked. |
| F5 | held | not touched: the added prompt text and the English keyword patterns do not fix the language the model writes in. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: name, price and rating in each pick still come from `product[...]`. |
| C4 | held | not touched |
| C5 | held | The cut `[:MAX_REASON_CHARS]` is unchanged and an empty reason is still kept; `+ pick["reason"] = ""` judges content, which is counted under F4. |
| C6 | held | not touched: the added check is regex only, with no second call or retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
