## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ return by_name.get(_key(text), " ".join(text.split()))`: a non-attendee owner is now kept as the model wrote it instead of `None`. The prompt's "write that person's full name exactly as in the list above" is a general rule the model still applies by reading. |
| F4 | held | not touched |
| C1 | held | not touched: items with no owner or no due date are still appended. |
| C2 | held | not touched |
| C3 | held | not touched: a rejected due date and one never given are both still `None`, the gap as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `items[:MAX_ITEMS]` still keeps 10, the gap as it was. |
| C6 | moved toward the model | `+ owner = _owner(fields[1], by_name)` feeds `seen` with `" ".join(text.split())` for a non-attendee: spacing is folded but case is not. The same task for "Marta Olsen" and "marta olsen" is now listed twice. |
| C7 | held | not touched |
| C8 | held | not touched: still one call, no retry, blank notes return early, malformed lines skipped. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
