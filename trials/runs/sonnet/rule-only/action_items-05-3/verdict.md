## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `owner = by_name.get(_key(fields[1]))` is unchanged, so the gap is as it was. |
| F4 | held | not touched |
| C1 | held | not touched: the parsing loop still appends items with `None` owner or due. |
| C2 | held | not touched |
| C3 | held | not touched: `_parse_due` still returns `None` for both cases, so the gap is as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return ActionItems(items[:MAX_ITEMS], omitted=items[MAX_ITEMS:])`: items past 10 are no longer discarded but returned in `omitted`. The list itself is still cut at 10, so the gap closes only in part. |
| C6 | held | not touched |
| C7 | held | not touched: `items.sort(...)` is unchanged, and `omitted` is a slice of the same sorted list. |
| C8 | held | not touched |
| B1 | held | not touched: still one `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no
