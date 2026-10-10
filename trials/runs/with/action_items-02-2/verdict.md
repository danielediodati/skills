## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is as it was. |
| F4 | moved toward code | `+ "by Friday" is the first Friday after the meeting, and "by next Friday" is the Friday of the following week. If the meeting itself falls on that day, it means a week later, never the day of the meeting.`: a rule in English that fixes the date, so the model no longer reads it in context. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still checks for a real date on or after the meeting. |
| C3 | held | not touched; the gap (rejected and never-given both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still a single `model(prompt)` call, and `+ calendar=_calendar(meeting_date),` only adds to the prompt. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no
