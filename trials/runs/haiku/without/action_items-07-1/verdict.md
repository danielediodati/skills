## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `- owner = by_name.get(_key(fields[1]))` → `+ owner = _owner(fields[1], by_name)` keeps a non-attendee's name as written, closing most of the gap. |
| F4 | held | not touched; the `due` instruction in the prompt is unchanged. |
| C1 | held | Items with owner `None` or due `None` are still appended; the change only widens which owners are kept. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; `_parse_due` still returns `None` for both rejected and absent dates, so the gap is as before. |
| C4 | held | not touched; `_clean_task` is unchanged. |
| C5 | held | not touched; `return items[:MAX_ITEMS]` remains, so the gap is as before. |
| C6 | held | `+ found = (_key(task), _key(owner) if owner else None)` still compares on case and spacing, now for non-attendee owners too. |
| C7 | held | not touched; the sort key is unchanged. |
| C8 | held | not touched; single call, empty-notes return, line-form skip and `NONE` handling are unchanged. |
| B1 | held | not touched; still one model call. |

## Trial

- where: both
- flagged: no
- stopped: no