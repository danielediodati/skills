## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `owner = by_name.get(_key(fields[1]))` is unchanged, so the gap stays as it was. |
| F4 | held | not touched |
| C1 | held | `- return items[:MAX_ITEMS]` / `+ return items`: undated and unowned items are still kept, and no longer cut from the end of the list. |
| C2 | held | not touched |
| C3 | held | not touched: `_parse_due` still returns `None` for both cases, so the gap stays as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return items`: the cap is gone, which closes the gap in full. |
| C6 | held | not touched |
| C7 | held | not touched: the `items.sort(...)` line is unchanged, only the slice after it was removed. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
