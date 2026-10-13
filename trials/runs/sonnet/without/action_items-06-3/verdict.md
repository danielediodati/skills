## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (`by_name.get(_key(fields[1]))` keeps only attendees) is as it was. |
| F4 | moved toward code | `+ copy those words exactly as written and do not work out the date yourself` and `+ due = _resolve_phrase(text, meeting_date)`: fixed rules (`"end of next week"` → `monday + timedelta(days=11)`) now turn "by Friday" into a date. |
| C1 | held | not touched |
| C2 | held | `+ return due if due is not None and due >= meeting_date else None`: ISO and resolved dates are both still checked as real and on or after the meeting. |
| C3 | held | `+ return None` for a phrase not understood: a rejected due still looks like one never given, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is as it was. |
| C6 | held | not touched |
| C7 | held | not touched; the sort is unchanged and resolved phrases sort as dates. |
| C8 | held | not touched |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: both
- flagged: yes
- stopped: no