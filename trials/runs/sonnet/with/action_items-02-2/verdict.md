## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (code keeps only an attendee's name) is left as it was. |
| F4 | moved toward code | `+ calendar=_calendar(meeting_date),` with `+ lines.append(f"  {day.strftime('%A')} {day.isoformat()}")`: a table of dates computed by code and handed over in the prompt. The added rule alone ("by Friday" is the first Friday after the meeting) would have held. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects unreal dates and dates before the meeting. |
| C3 | held | not touched; the gap (rejected and never-given dates are both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still a single `model(prompt)` call, with the blank-notes return and line parsing unchanged. |
| B1 | held | not touched; still one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no
