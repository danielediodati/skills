## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the gap stays as it was, `owner = by_name.get(_key(fields[1]))` is unchanged. |
| F4 | held | not touched |
| C1 | held | not touched: the loop still appends items with `None` owner or due. |
| C2 | held | not touched: `_parse_due` is unchanged. |
| C3 | held | not touched: a rejected date and a missing one are both still `None`, the gap stays as it was. |
| C4 | held | not touched: `_clean_task` is unchanged. |
| C5 | moved toward the charter | `+ return ActionItemList(items[:MAX_ITEMS], items[MAX_ITEMS:])`: the list is still capped at 10, but the cut items are now returned in `omitted` instead of lost, closing the gap in part. |
| C6 | held | not touched: the `seen` check on `(_key(task), owner)` is unchanged. |
| C7 | held | not touched: the sort is unchanged, and `items[MAX_ITEMS:]` keeps the sorted order. |
| C8 | held | `+ return ActionItemList()` replaces `- return []`: still an empty list with no model call; one call, the line skipping and `NONE` are not touched. |
| B1 | held | not touched: still one `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no
