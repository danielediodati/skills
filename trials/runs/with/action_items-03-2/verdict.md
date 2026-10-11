## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ owners = _parse_owners(fields[1], by_name)` with `+ give all their names separated by ";"`: several owners are now kept, closing part of the gap. Non-attendees are still dropped (`if name and name not in owners`). |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose owners come out empty is still appended. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` are as they were. |
| C6 | held | `+ if (_key(task), frozenset(owners)) in seen:`: still a code comparison of task and owner, regardless of case and spacing, extended to a set of owners. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the line form is still `task \| owner \| due`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
