## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if several people took it together, all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners are now kept, closing part of the gap. Non-attendees are still dropped. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item left with no owner still stays, with `owners` as `()`. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is left as it was. |
| C6 | held | `+ if (_key(task), frozenset(owners)) in seen:`: the same task for the same owners is still listed once, compared by code on case- and spacing-folded task and canonical names. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
