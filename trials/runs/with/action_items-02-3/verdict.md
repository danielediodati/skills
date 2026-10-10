## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name is kept) is as it was. |
| F4 | moved toward code | `+ A bare weekday ("by Friday") is the first such day after the meeting, never the meeting day itself. With "next" ... it is that weekday in the week after`: the prompt fixes the date, so the model can no longer read it in context. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still checks a real date on or after the meeting. |
| C3 | held | not touched; the gap (both set to `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` still caps at 10, so the gap is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; `+ weekday=_WEEKDAYS[meeting_date.weekday()],` only adds to the one prompt. |
| B1 | held | not touched; still one model call. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
