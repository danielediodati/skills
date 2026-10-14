## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the owner mapping `by_name.get(_key(fields[1]))` is unchanged, so the gap stays as it was. |
| F4 | moved toward code | `+ due = _resolve_phrase(_BY.sub("", _key(text)), meeting_date)` with `_WEEKDAY`/`_END_OF_WEEK` rules: code now turns "by Friday" and "end of next week" into dates, which the line leaves to the model's reading. |
| C1 | held | Unresolved phrases still give `due = None` and the item is kept; owner handling is not touched. |
| C2 | held | `+ if due is None or due < meeting_date: return None` still rejects dates before the meeting, for ISO and resolved dates alike. |
| C3 | held | not touched; rejected and absent dates both still give `None`, so the gap stays as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `items[:MAX_ITEMS]` still caps the list, so the gap stays as it was. |
| C6 | held | not touched |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | not touched; still one call, blank notes return early, and malformed lines are skipped. |
| B1 | held | not touched; still one model call. |

## Trial

- where: both
- flagged: no
- stopped: no