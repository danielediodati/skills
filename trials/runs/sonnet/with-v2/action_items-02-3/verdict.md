## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name is kept) is left as it was. |
| F4 | held | `+ Read "by Friday" as the first Friday after the meeting, and "by next Friday" as the Friday of the following week.`: a general reading rule the model still applies to each note. `+ weekday=meeting_date.strftime("%A")` gives a fact about the meeting, not the due date. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects unreal dates and dates before the meeting. |
| C3 | held | not touched; the gap (a rejected date and one never given are both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the added weekday and rule inside the same prompt. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
