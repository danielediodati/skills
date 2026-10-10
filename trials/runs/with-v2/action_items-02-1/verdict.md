## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the gap (only an attendee's name kept, anyone else `None`) is as it was. |
| F4 | moved toward code | `+ "by Friday" means the first Friday after the day of the meeting ... If the meeting is held on that same weekday, the date meant is a week later`: a rule in the prompt fixes the date, so the model can no longer read it in context. |
| C1 | held | not touched |
| C2 | held | not touched: `_parse_due` still checks for a real date on or after the meeting. |
| C3 | held | not touched: the gap (rejected and never-given dates both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched: the gap (`MAX_ITEMS = 10`) is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched: `+ weekday=meeting_date.strftime("%A")` only adds to the one prompt; still one call, no retry. |
| B1 | held | not touched: still one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no
