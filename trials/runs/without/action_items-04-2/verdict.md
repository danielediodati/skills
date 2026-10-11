## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = by_name.get(_key(fields[1])) or _match_attendee(fields[1], attendees)`: a prefix/initial rule in code now decides which attendee a name means. Prompt adds `or it is not clear which attendee did`, and non-attendees are still set to `None`. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap stays as it was |
| C4 | held | not touched |
| C5 | held | not touched; the gap stays as it was |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
