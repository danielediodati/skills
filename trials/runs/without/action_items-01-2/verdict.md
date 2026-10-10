## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ If it fits more than one, write "none".` dictates the outcome, and `+ return matches[0] if len(matches) == 1 else None` adds a code rule that rewrites the model's owner. The owner is still attendee-or-`None`, never free text as the notes give it. |
| C1 | held | not touched: an item whose owner resolves to `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap stays as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` stays, so the gap is as it was. |
| C6 | held | not touched: `(_key(task), owner) in seen` is unchanged; only the owner fed into it comes from `_resolve_owner`. |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call, with the same line parsing. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
