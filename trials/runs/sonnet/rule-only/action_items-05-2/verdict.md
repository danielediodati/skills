## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return Extraction(items[:MAX_ITEMS], items[MAX_ITEMS:])` and `+ warnings.warn(...)`: items past 10 are now returned and announced, not discarded. The gap closes only in part: `extract_action_items` still returns `result.items`, capped at 10. |
| C6 | held | not touched |
| C7 | held | not touched; `items.sort(...)` is unchanged and the split into `items` and `omitted` comes after it. |
| C8 | held | `- return []` / `+ return Extraction([], [])`: empty notes still return an empty list without calling the model. `extract_action_items` makes one call to `extract_with_omitted`, so still one model call. |
| B1 | held | not touched; still one `model(prompt)` call per set of notes. |

## Trial

- where: code
- flagged: yes
- stopped: no
