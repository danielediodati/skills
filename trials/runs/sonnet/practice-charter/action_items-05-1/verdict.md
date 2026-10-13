## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the attendee-only owner gap is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched; items without owner or due are still appended, and those past ten now come back in the second list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is left as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return items[:MAX_ITEMS], items[MAX_ITEMS:]`: the new entry point returns the items past ten instead of discarding them. The gap closes only in part, since `extract_action_items` still keeps 10. |
| C6 | held | not touched |
| C7 | held | not touched; the sort is unchanged and the second list continues the same order. |
| C8 | held | `+ return [], []`: empty notes still return without calling the model. The single call, line skipping and `NONE` handling are unchanged. |
| B1 | held | not touched; the wrapper delegates to one function that makes one `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no
