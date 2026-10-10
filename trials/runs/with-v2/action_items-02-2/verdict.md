## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+ "by Friday" is the first Friday after the meeting, and "by next Friday" is the Friday of the following week. If the meeting itself falls on that weekday, "by Friday" means a week later`: a fixed rule in the prompt, so the model can no longer read the weekday in context. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still requires a real date on or after the meeting. |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; `+ weekday=meeting_date.strftime("%A"),` only adds a fact to the single prompt, with no extra call or retry. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
