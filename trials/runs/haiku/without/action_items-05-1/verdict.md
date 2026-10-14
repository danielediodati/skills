## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap stays as it was (`by_name.get(_key(fields[1]))` unchanged). |
| F4 | held | not touched |
| C1 | held | not touched; items without owner or due are still appended to `items`. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; the rejected-date and never-given cases still both give `None`. |
| C4 | held | not touched; `_clean_task` and `MAX_TASK_CHARS` are unchanged. |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return Extraction(items=items, skipped=skipped)`: the cap of 10 is gone. |
| C6 | held | not touched; the `seen` check on `(_key(task), owner)` is unchanged. |
| C7 | held | not touched; the `items.sort(...)` key is unchanged. |
| C8 | held | Malformed lines are still left out of `items` (`+ skipped.append(raw.strip())`) and `NONE` still gives no items (`+ if answer.strip().upper() == "NONE": return Extraction(items=[], skipped=[])`). One call, no retry, and empty notes return early. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no