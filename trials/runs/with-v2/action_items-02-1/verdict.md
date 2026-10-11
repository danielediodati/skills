## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the "Not yet in code" gap (attendee-only owner) is left as it was. |
| F4 | held | `+ A day of the week is a deadline: "by Friday" means the first Friday after the day of the meeting`: a general reading rule the model still applies to each note. `+ weekday=meeting_date.strftime("%A")` hands over the meeting's weekday, not the due date. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects unreal dates and dates before the meeting. |
| C3 | held | not touched; the "Not yet in code" gap (rejected and never-given both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the "Not yet in code" gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the same line parsing and `NONE` handling. |
| B1 | held | not touched; still one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no
