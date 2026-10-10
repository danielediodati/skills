## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people took it together, write all their names separated by semicolons` and `+ owners = _parse_owners(fields[1], by_name)`: several owners are now kept, closing part of the gap. Non-attendees are still dropped (`if name is not None and name not in owners`). |
| F4 | held | not touched |
| C1 | held | `+ ActionItem(task, owners[0] if owners else None, due, owners)`: an item with no recognised owner is still appended with `owner` `None`. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (both set to `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` is left as it was. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the case- and spacing-folded task plus canonical attendee names. Single-owner behaviour is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched; the prompt addition keeps the `task \| owner \| due` form ("still on the same line") and there is still one call. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
