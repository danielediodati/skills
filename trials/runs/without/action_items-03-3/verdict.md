## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people share the task, write all their names separated by ";"` and `+ owners = _parse_owners(fields[1], by_name)`: several owners are now kept, which closes part of the gap. Non-attendees are still dropped (`if name is not None and name not in owners`), as before. |
| F4 | held | not touched |
| C1 | held | `+ first = owners[0] if owners else None`: an item with no recognised owner still stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` still caps at 10, the gap is as it was. |
| C6 | held | `+ if (_key(task), owners) in seen:`: still a code comparison on the task key and attendee-canonical names, so case and spacing are ignored. It now compares the whole owner tuple. |
| C7 | held | not touched |
| C8 | held | not touched; still one call, and the `rsplit("|", 2)` form check, blank-notes return and `NONE` handling are unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
