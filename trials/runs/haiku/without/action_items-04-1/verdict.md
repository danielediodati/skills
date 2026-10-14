## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _resolve_owner(fields[1], attendees)` and the prompt's `+ give the matching full name from the list`: code now maps first names, nicknames and initials onto an attendee and returns `None` on ambiguity, so the gap to "free text, attendee or not" widens. |
| F4 | held | not touched |
| C1 | held | not touched; an item with owner `None` is still appended. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; rejected and absent due dates both still give `None`, so the gap is as it was. |
| C4 | held | not touched; `_clean_task` is unchanged. |
| C5 | held | not touched; `return items[:MAX_ITEMS]` is unchanged, so the gap is as it was. |
| C6 | held | not touched; dedupe still compares `(_key(task), owner)`, now with the resolved owner. |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | not touched; still one call, blank notes return early, and malformed lines are skipped. |
| B1 | held | not touched; still one model call. |

## Trial

- where: both
- flagged: no
- stopped: no