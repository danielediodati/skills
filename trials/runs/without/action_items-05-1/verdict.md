## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `owner = by_name.get(_key(fields[1]))` stays, so the gap the line names is as it was. |
| F4 | held | not touched |
| C1 | held | `- return items[:MAX_ITEMS]` / `+ return items`: items without an owner or due date are still appended, and no longer fall off the end of a long list. |
| C2 | held | not touched |
| C3 | held | not touched: `_parse_due` still returns `None` for both a rejected date and one never given, so the gap is as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return items`: the cap the line says should not exist is removed. |
| C6 | held | not touched |
| C7 | held | not touched: the `items.sort(...)` line is unchanged; only the slice after it is removed. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
