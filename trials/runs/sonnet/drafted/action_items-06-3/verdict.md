## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is as it was. |
| F4 | moved toward code | `+ calendar=_calendar(meeting_date)` with `+ work out the date from the calendar above`: a table of dates computed by code is handed to the model, so code does the weekday-to-date step the line leaves to reading. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; a rejected date and one never given are both still `None`. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` still keeps 10. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with blank notes, malformed lines and `NONE` handled as before. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no