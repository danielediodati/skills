## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ return by_name.get(_key(owner), owner)` keeps a non-attendee or several owners as written instead of `None`. The prompt's "write their name exactly as in the list above" is a general rule the model still applies by reading. |
| F4 | held | not touched |
| C1 | held | `+ if _key(owner) in _EMPTY: return None`: an ownerless item still gets `owner=None` and is appended, not dropped. |
| C2 | held | not touched |
| C3 | held | not touched; a rejected date and one never given still both come out as `None`, the gap as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` still keeps 10, the gap as it was. |
| C6 | moved toward the model | `+ return by_name.get(_key(owner), owner)` feeds the unchanged `(_key(task), owner) in seen`: a non-attendee owner is now compared in the model's own casing, so "Marta Olsen" and "marta olsen" list the same task twice. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, blank notes return early, malformed lines skipped, `NONE` gives no items. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: both
- flagged: no
- stopped: no
