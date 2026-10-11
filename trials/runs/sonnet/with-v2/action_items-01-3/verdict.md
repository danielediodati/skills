## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = by_name.get(_key(fields[1])) or by_first.get(_key(fields[1]))` with `_unique_first_names`: a lookup table now rewrites the model's "Priya" to an attendee, where the line wants the owner as the notes give it. Non-attendees and several owners still become `None`, so the gap is not closed, and code takes a new decision on who the owner is. |
| F4 | held | not touched |
| C1 | held | not touched: an item whose owner resolves to nothing is still appended with `owner` set to `None`. |
| C2 | held | not touched |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `MAX_ITEMS` still applies, the gap is left as it was. |
| C6 | held | not touched: `seen` still keys on `(_key(task), owner)`; only the owner value fed into it comes from the new lookup. |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call, with the same skipping and `NONE` handling. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: no
