## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: `PROMPT` is unchanged, so the model still decides what counts as an action item. |
| F2 | held | not touched: the task wording stays the model's own and `_clean_task` is unchanged. |
| F3 | held | not touched: `owner = by_name.get(_key(fields[1]))` is as before, so the "Not yet in code" gap is neither closed nor widened. |
| F4 | held | not touched: the model still reads the deadline and `_parse_due` is unchanged. |
| C1 | held | not touched: the parsing loop still appends items with no owner or due date; the cut of undated items is the old cap, judged under C5. |
| C2 | held | not touched: `return due if due >= meeting_date else None` is unchanged. |
| C3 | held | not touched: a rejected date and one never given are both still `None`; the gap is as it was. |
| C4 | held | not touched: `_clean_task` and `MAX_TASK_CHARS` are unchanged. |
| C5 | held | `+ return Extraction(items[:MAX_ITEMS], max(0, len(items) - MAX_ITEMS))`: the cap of 10 still cuts the list in both functions. `omitted` counts the cut but lifts nothing, so the gap is as it was. |
| C6 | held | not touched: the `seen` check on `(_key(task), owner)` is unchanged, and `omitted` is counted after it. |
| C7 | held | not touched: `items.sort(key=lambda item: (item.due is None, item.due or date.max))` is unchanged. |
| C8 | held | `+ return Extraction([], 0)` with `.items` still gives `[]` for empty notes without calling the model. One call, no retry, and the line parsing is unchanged. |
| B1 | held | not touched: `extract_action_items` delegates to `extract_with_report`, which calls `model(prompt)` once. |

## Trial

- where: code
- flagged: yes
- stopped: partial