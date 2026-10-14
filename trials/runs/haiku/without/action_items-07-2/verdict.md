## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ if re.search(rf"(?<!\w){re.escape(_key(name))}(?!\w)", notes_key): return name`: a non-attendee owner now survives, but only if the notes contain the name, so the gap is only partly closed. |
| F4 | held | not touched |
| C1 | held | not touched; items with owner `None` or due `None` are still appended. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; rejected and absent dues both still give `None`, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` is still 10 and the gap is as it was. |
| C6 | held | `+ owner_key = _key(owner) if owner else None` keeps the dedupe case- and spacing-insensitive on both task and owner. |
| C7 | held | not touched |
| C8 | held | not touched; still one call, blank notes return early, malformed lines are skipped. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no