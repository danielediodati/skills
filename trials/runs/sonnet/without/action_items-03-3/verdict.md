## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people share the task, write all their names separated by ";"` and `+ items.append(ActionItem(task, first, due, owners[1:]))`: several owners are now kept, closing part of the gap. Non-attendees are still dropped (`if name is not None and name not in owners`), so the rest remains. |
| C1 | held | `+ first = owners[0] if owners else None`: an item with no recognised owner is still appended; the due date path is not touched. |
| C2 | held | not touched |
| C3 | held | not touched; the gap stays as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` stay as they were. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the case- and space-folded task and canonical attendee names. The tuple is ordered, so the same pair in a different order is not merged; the line does not cover several owners. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the `len(fields) != 3` skip is unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
