## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if several people took it together, all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners now survive, closing part of the gap. Non-attendees are still dropped (`name = by_name.get(_key(part))`). |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose `owners` is empty is still appended, as `owner=None` was before. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` is as it was. |
| C6 | held | `+ if (_key(task), frozenset(owners)) in seen:`: still a comparison made by code, on the task key and the owners, now as a set. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the line-form and `NONE` handling are unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
