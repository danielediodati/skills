## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: code still keeps only an attendee's name and sets anyone else to `None`; the gap is as it was. |
| F4 | held | not touched |
| C1 | held | not touched: the parsing loop still keeps items with no owner or due date. |
| C2 | held | not touched |
| C3 | held | not touched: a rejected date and one never given are both still `None`; the gap is as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return items`: the cap is gone, closing the gap in full. |
| C6 | held | not touched |
| C7 | held | not touched: the `items.sort(...)` line is unchanged; only the slice after it was removed. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
