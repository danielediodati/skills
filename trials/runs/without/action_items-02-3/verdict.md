## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the gap (only an attendee's name kept, anyone else `None`) is as it was. |
| F4 | moved toward code | `+  A day of the week is a deadline. Use this table, do not work it out yourself:` with `+{weekdays}` built by `_weekday_table`: code computes the date for "by Friday" and "next Friday", and the model only picks a row. |
| C1 | held | not touched |
| C2 | held | not touched: `_parse_due` is unchanged. |
| C3 | held | not touched: a rejected date and one never given are both still `None`. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` is unchanged. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call; the change only adds `meeting_weekday=` and `weekdays=` to `PROMPT.format`. |
| B1 | held | not touched: one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no
