## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people took it together, give all their names on the same line, separated by ";".` and `+ owners: Tuple[str, ...]`: several owners are now kept. The attendee-only part of the gap stays as it was (`name = by_name.get(_key(part))`). |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item with no known owner still stays, now with `owners` as `()`. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is as it was. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the task key and the attendee spellings. The tuple is ordered, so the same owners in a different order would not match. |
| C7 | held | not touched |
| C8 | held | not touched; still one call, and the line form is still `task \| owner \| due`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
