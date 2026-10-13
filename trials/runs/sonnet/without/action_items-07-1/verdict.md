## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if owner is None and _key(name) not in _EMPTY and _key(name) in notes_key:` / `+ owner, absent = name, True`: a non-attendee owner is now kept. The gap closes only in part: the name must appear verbatim in the notes. |
| F4 | held | not touched |
| C1 | held | not touched: an item whose owner resolves to `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `MAX_ITEMS` gap is left as it was. |
| C6 | broken by a slip | `+ owner, absent = name, True` feeds the unchanged `seen.add((_key(task), owner))`: an absent owner is compared with case as the model wrote it, so "Marta Olsen" and "marta olsen" list the same task twice. |
| C7 | held | not touched |
| C8 | held | not touched: still one call, same line parsing. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no