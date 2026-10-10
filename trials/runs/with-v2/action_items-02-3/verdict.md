## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+ Read "by Friday" as the first Friday after the meeting, and "by next Friday" as the Friday of the following week.`: the prompt fixes the date, so the model can no longer read it in context. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects unreal dates and dates before the meeting. |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the blank-notes return, line skipping and `NONE` unchanged. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
