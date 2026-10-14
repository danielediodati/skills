## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap stays as it was (`by_name.get(_key(fields[1]))` still sets non-attendees to `None`). |
| F4 | moved toward code | `+ Copy the words; do not work out a date yourself.` and `+ if phrase == "end of next week": return _next_monday(meeting_date) + timedelta(days=4)`: code now turns "Friday" and "end of next week" into dates by fixed rules, where the line leaves that reading to the model. |
| C1 | held | not touched; an unresolved deadline still gives `due` `None` and the item stays. |
| C2 | held | `+ return due if due and due >= meeting_date else None`: still a real date, on or after the meeting. |
| C3 | held | not touched; unresolvable or past dates still become `None`, the same as an absent date, so the gap is unchanged. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` still caps at 10, so the gap is unchanged. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one call, and `NONE`, the empty-notes return and the skipping of malformed lines are all unchanged. |
| B1 | held | not touched; still one model call. |

## Trial

- where: both
- flagged: no
- stopped: no