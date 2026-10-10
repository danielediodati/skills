## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+ If the notes give only a day of the week, do not work out the date: write the day as said` and `+ due = _weekday_due(text, meeting_date)`: a fixed rule in code now turns "by Friday" into a date. |
| C1 | held | not touched |
| C2 | held | `+ return due if due is not None and due >= meeting_date else None`: the real-date and on-or-after-the-meeting check still applies, to resolved weekdays too. |
| C3 | held | not touched; a rejected due date and one never given are both still `None` (`+ if not match or match.group(2) not in _WEEKDAYS: return None`), so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` remains, so the gap is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: both
- flagged: no
- stopped: no
