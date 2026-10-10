## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _resolve_owner(fields[1], attendees)` with `+ if len({_key(name) for name in matches}) == 1: return matches[0]`: a new code rule decides who a partial name is, rewrites "Priya" to the attendee's name and sets an ambiguous "Tom" to `None`. The gap is not closed: non-attendees and several owners still become `None`. |
| C1 | held | not touched: `_resolve_owner` returns `None` for an unknown or ambiguous owner and the item is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` is left as it was. |
| C6 | held | not touched: the comparison is still `(_key(task), owner) in seen`, now on the owner returned by `_resolve_owner`. |
| C7 | held | not touched |
| C8 | held | not touched: `answer = model(prompt)` is still the single call, and the prompt is unchanged. |
| B1 | held | not touched: one model call per set of notes. |

## Trial

- where: code
- flagged: no
- stopped: no
