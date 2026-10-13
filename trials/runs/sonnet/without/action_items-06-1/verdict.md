## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the "Not yet in code" gap (non-attendee owner set to `None`) is left as it was. |
| F4 | moved toward code | `+ copy those words exactly as written in the notes and do not work out the date yourself` and `+ due = _resolve_relative(text, meeting_date)`: fixed rules and a phrase table now turn "by Friday" into a date. |
| C1 | held | not touched |
| C2 | held | `+ return due if due is not None and due >= meeting_date else None`: the real-date and on-or-after-meeting check still applies, including to dates code resolves. |
| C3 | held | `+ return None` at the end of `_resolve_relative`: an unrecognised phrase still becomes `None`, same as one never given; the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, no retry. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: both
- flagged: no
- stopped: no