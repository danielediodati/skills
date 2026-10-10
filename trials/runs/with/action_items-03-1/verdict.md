## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if several people took it together, all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners now survive. Gap closed in part only: `by_name.get(_key(part))` still drops non-attendees. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose owners come back `()` is still appended, not dropped. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was, `_parse_due` still returns `None` for both cases. |
| C4 | held | not touched |
| C5 | held | not touched; the gap is as it was, `return items[:MAX_ITEMS]` still keeps 10. |
| C6 | held | `+ if (_key(task), frozenset(owners)) in seen:`: still a code comparison on the case- and spacing-folded task and the same owners, listed once. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the line form stays `task \| owner \| due`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
