## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people share the task, give all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners are now kept, closing part of the gap. Non-attendees are still dropped (`name = by_name.get(_key(part))`), so that part of the gap is as it was. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item with no known owner stays in the list with `owners` as an empty tuple. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` is unchanged, so the gap is as it was. |
| C6 | held | `+ if (_key(task), frozenset(owners)) in seen:`: still a code comparison on the case- and spacing-folded task and the resolved owners, now a set so name order does not matter. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and lines are still split with `rsplit("\|", 2)` into `task \| owner \| due`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
