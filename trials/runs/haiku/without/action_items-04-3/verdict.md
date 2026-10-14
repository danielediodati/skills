## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _find_owner(fields[1], attendees)` with nickname-prefix, surname and initial rules, and `return matches[0] if len(matches) == 1 else None`: code now decides which attendee a name is, and sets ambiguous names to `None`, where the line leaves the owner as free text. |
| F4 | held | not touched |
| C1 | held | not touched; an unresolved or ambiguous owner still keeps the item with `owner` `None`. |
| C2 | held | not touched |
| C3 | held | not touched; the gap stays as it was (`_parse_due` unchanged). |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` cap unchanged. |
| C6 | held | not touched; the `(_key(task), owner)` comparison is unchanged, only the owner is now resolved first. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: both
- flagged: no
- stopped: no