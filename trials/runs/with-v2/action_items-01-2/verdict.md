## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ matches = [name for k, name in by_name.items() if words <= set(k.split())]` / `+ return matches[0] if len(matches) == 1 else None`: a new word-match rule in code decides which person a partial name means and overrides the model's text. Non-attendees and several owners still become `None`. |
| F4 | held | not touched |
| C1 | held | `+ return matches[0] if len(matches) == 1 else None`: an ambiguous or unmatched owner becomes `None` and the item is still appended. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (both set to `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` are as they were. |
| C6 | held | `+ owner = _resolve_owner(fields[1], by_name)`: the `seen` check is unchanged and still compares `(_key(task), owner)`, now on the resolved owner. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: no
