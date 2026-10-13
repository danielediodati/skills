## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | held | `+ "By Friday" is the deadline on that Friday itself, not the day before.` and `+ weekday=_WEEKDAYS[meeting_date.weekday()],`: definitions of how to read a phrase plus a fact about the meeting; the model still works out each date. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; the gap (a rejected date and one never given both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with no retry added. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no