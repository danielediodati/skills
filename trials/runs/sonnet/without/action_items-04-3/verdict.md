## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _resolve_owner(fields[1], attendees)` with `+ return matches[0] if len(matches) == 1 else None`: a new code rule picks which attendee a short name means. Non-attendees and several owners still become `None`, so the gap is not closed but built on. |
| F4 | held | not touched |
| C1 | held | not touched: an item whose owner `_resolve_owner` returns as `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap stays as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` stays, the gap as it was. |
| C6 | held | not touched: `(_key(task), owner) in seen` unchanged, now compared on the resolved owner. |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call, and the same skipping of malformed lines. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
