## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ owners = _parse_owners(fields[1], by_name)` and `+ If several people took it together, write all their names separated by ";"`: several owners now survive. Non-attendees are still dropped (`by_name.get(_key(part))`), so the gap closes only in part. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))`: an item whose `owners` is `()` or whose `due` is `None` still stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` is unchanged, so the gap is as it was. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on case- and spacing-normalised task plus canonical owner names. The tuple is order-sensitive for shared owners. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, the blank-notes return and the `len(fields) != 3` skip are unchanged. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: both
- flagged: no
- stopped: no
