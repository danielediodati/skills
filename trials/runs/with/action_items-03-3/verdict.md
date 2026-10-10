## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if several people took it together, all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners now kept, closing part of the gap. Non-attendees are still dropped, as before. |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose `owners` is empty still stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched; a rejected due date and one never given are both still `None`, the gap as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` remain, the gap as it was. |
| C6 | held | `+ if (_key(task), frozenset(owners)) in seen:`: still a code comparison of task and owners, regardless of case and spacing, now over the set of owners. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the `len(fields) != 3` skip is unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
