## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ matches = [name for attendee, name in by_name.items() if set(words) <= set(attendee.split())]` and `+ return matches[0] if len(matches) == 1 else None`: code now also resolves which person a partial name means, overriding the model's free text. The attendee-only gap stays and widens. |
| C1 | held | `+ return matches[0] if len(matches) == 1 else None`: an ambiguous or unmatched owner becomes `None` and the item is still appended. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (both set to `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | Comparison not touched: `(_key(task), owner) in seen` is unchanged and only receives the owner from `+ owner = _resolve_owner(fields[1], by_name)`. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the parsing is unchanged. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
