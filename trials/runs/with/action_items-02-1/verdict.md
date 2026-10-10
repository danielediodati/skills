## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+ "by Friday" means the first Friday after the meeting date (a week later if the meeting itself is on a Friday). "by next Friday" means the Friday of the following week.`: a rule in English that fixes which date a weekday maps to, so the model no longer reads it in context. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects unreal dates and dates before the meeting. |
| C3 | held | not touched; the gap (rejected and never-given both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; `+ weekday=meeting_date.strftime("%A"),` only adds a field to the single prompt. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
