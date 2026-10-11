## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+ If the notes give only a day of the week, do not work out the date` and `+ due = _weekday_due(text, meeting_date)`: code, not the model, turns "by Friday" into a date. |
| C1 | held | not touched |
| C2 | held | `+ return due if due is not None and due >= meeting_date else None`: the real-date and on-or-after-meeting check still applies to every due date. |
| C3 | held | `+ if not match or match.group(2) not in _WEEKDAYS:` / `return None`: a rejected due date still becomes `None`, same as one never given; gap unchanged. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` remain, gap unchanged. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, no retry. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
