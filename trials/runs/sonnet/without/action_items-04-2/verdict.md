## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = by_name.get(_key(fields[1])) or _match_attendee(fields[1], attendees)`: a prefix/initial rule now picks the attendee, still attendees only. `+ Write "none" only if nobody took it, or it is not clear which attendee did` widens the gap. |
| F4 | held | not touched |
| C1 | held | not touched: an item whose owner resolves to `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `MAX_ITEMS` is unchanged, the gap is left as it was. |
| C6 | held | not touched: `(_key(task), owner)` still compares regardless of case and spacing, now on the resolved owner. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched: still one `model(prompt)` call. |

## Trial

- where: both
- flagged: no
- stopped: no
