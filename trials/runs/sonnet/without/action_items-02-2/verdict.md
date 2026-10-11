## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the gap stays as it was, `by_name.get(_key(fields[1]))` still keeps only an attendee's name. |
| F4 | moved toward code | `+ The next two weeks are:` / `+{calendar}` is a table of dates computed by code and handed over in the prompt. `+ due = _weekday_due(text, meeting_date)` has code turn "by Friday" into a date. |
| C1 | held | not touched |
| C2 | held | `+ return due if due >= meeting_date else None` keeps the check, and it also applies to dates from `_weekday_due`. |
| C3 | held | `+ if due is None:` / `+ return None`: a rejected date and one never given are both still `None`, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched: the gap stays as it was, `items[:MAX_ITEMS]` still keeps 10. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call, with no retry. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
