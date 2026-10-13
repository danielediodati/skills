## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `- owner = by_name.get(_key(fields[1]))` / `+ return by_name.get(key) or " ".join(text.split())`: a non-attendee owner is now kept as the model wrote it instead of set to `None`. The prompt's "when that clearly means one of the people present" is a rule the model still applies by reading. |
| F4 | held | not touched |
| C1 | held | `+ if key in _EMPTY: return None` then `items.append(ActionItem(task, owner, due))`: an item with no owner or no due date still stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched: a rejected due date and one never given are both still `None`, the gap as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `return items[:MAX_ITEMS]` is still there, the gap as it was. |
| C6 | held | `+ owner_key = _key(owner) if owner else None` / `+ if (_key(task), owner_key) in seen:`: free-text owners are still compared regardless of case and spacing. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched: still one `model(prompt)` call. |

## Trial

- where: both
- flagged: no
- stopped: no
