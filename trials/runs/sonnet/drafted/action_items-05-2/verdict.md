## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the attendee lookup `by_name.get(_key(fields[1]))` is unchanged, so the gap is as it was. |
| F4 | held | not touched |
| C1 | held | not touched: items without an owner or a due date are still appended to the list. |
| C2 | held | not touched |
| C3 | held | not touched: `_parse_due` still returns `None` in both cases, so the gap is as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return Extraction(items[:MAX_ITEMS], items[MAX_ITEMS:])`: items past the cap are now returned in `omitted` rather than discarded. The gap closes only in part, since `items` and `extract_action_items` still keep 10. |
| C6 | held | not touched |
| C7 | held | not touched: the sort is unchanged and `omitted` follows the same order. |
| C8 | held | `+ return Extraction([], [])`: empty notes still return an empty list without calling the model, through `.items`. Still one call, and parsing is unchanged. |
| B1 | held | not touched: still one `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no