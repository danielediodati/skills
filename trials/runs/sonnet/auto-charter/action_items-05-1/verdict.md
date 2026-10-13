## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: code still keeps only an attendee's name, so the gap is as it was. |
| F4 | held | not touched |
| C1 | held | not touched: the parsing loop still keeps items with no owner or due date. |
| C2 | held | not touched |
| C3 | held | not touched: a rejected date and one never given are both still `None`, so the gap is as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `-MAX_ITEMS = 10` `+MAX_ITEMS = 25` and `+ kept.omitted = len(items) - len(kept)`: the cap is looser and its cut is now reported, but a cap remains where the line says none. |
| C6 | held | not touched |
| C7 | held | not touched: the sort is unchanged, and `+ kept = ActionItems(items[:MAX_ITEMS])` keeps the sorted order. |
| C8 | held | `- return []` `+ return ActionItems()`: empty notes still return an empty list without calling the model; one call, no retry. |
| B1 | held | not touched: still one `model(prompt)` call per set of notes. |

## Trial

- where: code
- flagged: no
- stopped: no
