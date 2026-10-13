## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `owner = by_name.get(_key(fields[1]))` is unchanged, so the gap is as it was. |
| F4 | held | not touched |
| C1 | held | not touched: items without an owner or due date are still appended. |
| C2 | held | not touched |
| C3 | held | not touched: `_parse_due` still returns `None` for both cases, so the gap is as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return ActionItemList(items[:MAX_ITEMS], items[MAX_ITEMS:])`: the list still keeps 10, but items past the cap are now returned in `.dropped` instead of discarded, which closes the gap in part. |
| C6 | held | not touched |
| C7 | held | not touched: `items.sort(...)` is unchanged, and `items[MAX_ITEMS:]` keeps the sorted order for the dropped items. |
| C8 | held | `- return []` / `+ return ActionItemList()`: still an empty list returned before the model is called; one call, line skipping and `NONE` are unchanged. |
| B1 | held | not touched: still a single `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no
