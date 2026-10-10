## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ if set(words) <= set(attendee.split())` and `+ return matches[0] if len(matches) == 1 else None`: a word-match rule now picks which attendee a partial name means and overwrites the model's text. The output is still only an attendee or `None`, so the gap is not closed. |
| F4 | held | not touched |
| C1 | held | not touched; an item whose owner resolves to `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (a rejected date and one never given are both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`items[:MAX_ITEMS]`) is as it was. |
| C6 | held | `+ owner = _resolve_owner(fields[1], by_name)` feeds the same `(_key(task), owner)` comparison; still a string comparison regardless of case and spacing. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the same line-form, `NONE` and empty-notes handling. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: code
- flagged: no
- stopped: no
