## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | held | not touched |
| C1 | held | Parsing not touched; `- return items[:MAX_ITEMS]` / `+ return items` only stops undated items being cut from the end. |
| C2 | held | not touched |
| C3 | held | not touched: the gap (rejected and never-given dates both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return items`: the cap is removed, closing the gap in full. |
| C6 | held | not touched |
| C7 | held | not touched: the `items.sort(...)` line is unchanged, only the slice after it is removed. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
