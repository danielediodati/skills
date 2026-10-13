## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (attendee-only owner, anyone else `None`) is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched; items without an owner or a due date are still appended as before. |
| C2 | held | not touched |
| C3 | held | not touched; a rejected due date and one never given are both still `None`. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return ActionItems(items[:MAX_ITEMS], omitted=items[MAX_ITEMS:])`: the items past the cap are now returned on `.omitted` instead of dropped. The gap closes only in part, since the list itself still stops at 10. |
| C6 | held | not touched |
| C7 | held | not touched; the sort is unchanged, and `omitted` is the tail of the same sorted list. |
| C8 | held | `+ return ActionItems()`: empty notes still return an empty list without calling the model. One call, line skipping and `NONE` are not touched. |
| B1 | held | not touched; still one model call. |

## Trial

- where: code
- flagged: yes
- stopped: no