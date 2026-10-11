## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | held | `+ "by Friday" is the first Friday after the meeting, and "by next Friday" is the Friday of the following week`: a definition of how to read a phrase, which the model still applies to each note. `+ weekday=meeting_date.strftime("%A")` hands over a fact, not the due date. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still checks for a real date on or after the meeting. |
| C3 | held | not touched; the gap (a rejected date and one never given are both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the added text inside the same prompt. |
| B1 | held | not touched; still one model call per set of notes. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
