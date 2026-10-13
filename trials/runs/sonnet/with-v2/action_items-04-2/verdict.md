## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ return by_name.get(_key(text), " ".join(text.split()))`: a non-attendee or several-name owner is now kept as the model wrote it instead of `None`. The prompt's "write that person's full name exactly as in the list above" still leaves the model to read who the owner is. |
| F4 | held | not touched |
| C1 | held | not touched: `_owner` returns `None` for an empty owner and the item is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap (rejected and never-given dates both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` is as it was. |
| C6 | broken by a slip | `if (_key(task), owner) in seen:` is left on the raw owner, while `_owner` now returns free text `" ".join(text.split())`. "Marta Olsen" and "marta olsen" on the same task are listed twice; `_key(owner)` in the seen key fixes it. |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call, and the same handling of empty notes, malformed lines and `NONE`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
