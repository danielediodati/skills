## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ matches = by_part.get(key, ())` / `+ if len(matches) == 1: return next(iter(matches))`: a lookup table now decides which attendee a bare name means and overrides the model's text. Non-attendees and several owners still become `None`, so the gap widens. |
| F4 | held | not touched |
| C1 | held | not touched; an unresolved or ambiguous owner still gives `return None` and the item is kept. |
| C2 | held | not touched |
| C3 | held | not touched; the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` gap is left as it was. |
| C6 | held | not touched; `if (_key(task), owner) in seen` is unchanged and is still a string comparison, now on the resolved owner. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the same line parsing. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
