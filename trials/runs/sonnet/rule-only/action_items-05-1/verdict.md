## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `owner = by_name.get(_key(fields[1]))` is unchanged, so the gap stays as it was. |
| F4 | held | not touched |
| C1 | held | Parsing not touched; items without owner or due are still kept, and those past the cap now land in `omitted` via `+ return ActionItemList(items[:MAX_ITEMS], items[MAX_ITEMS:])`. |
| C2 | held | not touched |
| C3 | held | not touched: `_parse_due` still returns `None` for both cases, so the gap stays as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return ActionItemList(items[:MAX_ITEMS], items[MAX_ITEMS:])`: the cap of 10 stays, but items past it are returned in `omitted` instead of discarded, closing the gap in part. |
| C6 | held | not touched |
| C7 | held | The sort is not touched; `items[MAX_ITEMS:]` keeps the omitted items in the same sorted order. |
| C8 | held | `- return []` / `+ return ActionItemList()`: still an empty list without calling the model; one call, line skipping and `NONE` are not touched. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: no
