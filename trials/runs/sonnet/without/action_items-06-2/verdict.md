## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is as it was. |
| F4 | moved toward code | `+ calendar=_calendar(meeting_date),` with `+ Read the deadline off the calendar above, do not count days yourself:`: a table of dates computed by code and handed over in the prompt. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; a rejected date and one never given are both still `None`. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the same line parsing and blank-notes return. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no