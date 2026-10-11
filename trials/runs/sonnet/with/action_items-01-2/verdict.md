## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ found = [name for name in attendees if words <= set(_key(name).split())]` / `+ return found[0] if len(found) == 1 else None`: a new code rule decides which attendee a partial name means and overrides the model's text. Non-attendees and several owners still become `None`. |
| C1 | held | not touched: an item whose owner `_match_owner` returns as `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` is left as it was. |
| C6 | held | The `seen` check is not touched; only its owner input changes, via `+ owner = _match_owner(fields[1], attendees)`. The comparison is still made by code, regardless of case and spacing. |
| C7 | held | not touched |
| C8 | held | not touched: the prompt and the single `model(prompt)` call are unchanged. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
