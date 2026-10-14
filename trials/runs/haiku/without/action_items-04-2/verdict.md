## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _resolve_owner(fields[1], attendees, aliases or {})`: code now decides which attendee a name means, via an `aliases` table, word and initial matching, and `None` for "Ana and Tom" or an ambiguous "Ana". The line leaves who the owner is to the model. |
| F4 | held | not touched |
| C1 | held | not touched; items with `owner` or `due` of `None` are still appended. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; rejected and absent due dates are both still `None`, so the gap is as it was. |
| C4 | held | not touched; `_clean_task` is unchanged. |
| C5 | held | not touched; `items[:MAX_ITEMS]` is unchanged, so the gap is as it was. |
| C6 | held | not touched; dedupe is still on `(_key(task), owner)`, with `owner` now resolved first. |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | not touched; still one call, an empty-notes early return, and non-form lines skipped. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: code
- flagged: no
- stopped: no