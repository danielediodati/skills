## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people took it together, write all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners now survive. The attendee-only filter (`by_name.get(_key(part))`) leaves the rest of the gap as it was. |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose `owners` ends up `()` is still appended, as one with `None` was before. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is as it was. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the task key and the canonical attendee spelling. The tuple is ordered, so the same pair in a different order is not merged, a case the line does not cover. |
| C7 | held | not touched |
| C8 | held | not touched; the `;` list sits inside the owner field, so the `task \| owner \| due` form and the single call are unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
