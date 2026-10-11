## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+  A day of the week is a deadline. Use this table, do not work it out` / `+        weekdays=_weekday_table(meeting_date),`: code computes the dates and the prompt hands them over, so the model no longer reads "by Friday" in context. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still checks for a real date on or after the meeting. |
| C3 | held | not touched; a rejected date and one never given are both still `None`, the gap left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` still caps at 10, the gap left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the same line parsing and `NONE` handling. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no
