## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ return by_name.get(key) or " ".join(text.split())` replaces `- owner = by_name.get(_key(fields[1]))`: a non-attendee owner is kept as the model wrote it. Prompt adds "when that clearly means one of the people present", which the model still applies by reading. |
| F4 | held | not touched |
| C1 | held | Not touched: `items.append(ActionItem(task, owner, due))` is unchanged, and `+ if key in _EMPTY: return None` still keeps an item with no owner. |
| C2 | held | not touched |
| C3 | held | Not touched: `_parse_due` still returns `None` for both cases, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | Not touched: `return items[:MAX_ITEMS]` is unchanged, so the gap is as it was. |
| C6 | held | `+ owner_key = _key(owner) if owner else None` and `+ if (_key(task), owner_key) in seen:`: free-text owners are still compared regardless of case and spacing. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
