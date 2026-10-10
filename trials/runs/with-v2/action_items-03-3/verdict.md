## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if several people took it together, give each name, separated by ";".` and `+ owners: Tuple[str, ...]`: several owners now survive, closing part of the gap. `_parse_owners` still drops non-attendees (`if name is not None`), so "attendee or not" stays open. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose owners come back as `()` is still appended, so it stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` are as they were. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the case- and space-folded task plus canonical attendee names. The tuple is order-sensitive, so the same pair in a different order would not be merged. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the `task \| owner \| due` line form, blank-notes return and `NONE` handling are unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: yes
- stopped: no
