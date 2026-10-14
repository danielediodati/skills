## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `- owner = by_name.get(_key(fields[1]))` / `+ owner, owner_present = _parse_owner(fields[1], by_name)`: a non-attendee's name is now kept as the model wrote it, closing most of the gap. |
| F4 | held | not touched |
| C1 | held | not touched; items with no owner or no due date still stay in the list. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; a rejected due date still becomes `None`, as before. |
| C4 | held | not touched; `_clean_task` is unchanged. |
| C5 | held | not touched; `items[:MAX_ITEMS]` is unchanged. |
| C6 | held | `+ owner_key = None if owner is None else _key(owner)` and `seen` now keys on `(_key(task), owner_key)`, so the comparison stays case- and spacing-insensitive. |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | not touched; still one call, no retry, and skipped lines, `NONE` and empty notes are handled as before. |
| B1 | held | not touched; still one model call per set of notes. |

## Trial

- where: both
- flagged: yes
- stopped: no