## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if several people took it together, give each name, separated by ";"` and `+ owners: Tuple[str, ...]`: several owners now survive, closing part of the gap. Non-attendees are still dropped (`if name is not None and name not in owners`), so that part of the gap stays as it was. |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose owners come out as `()` still stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is left as it was. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the case- and spacing-folded task and the canonical attendee names. The tuple is order-sensitive, so the same pair in a different order would not be merged. |
| C7 | held | not touched |
| C8 | held | not touched; still one call, and the line form is still `task \| owner \| due`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
