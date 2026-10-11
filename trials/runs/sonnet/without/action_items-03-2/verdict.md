## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people took it together, write all their names separated by semicolons` and `+ owners = _parse_owners(fields[1], by_name)`: several owners now survive, closing the "one person or several" part of the gap. `by_name.get(_key(part))` still drops non-attendees, so the gap is only partly closed. |
| F4 | held | not touched |
| C1 | held | `+ ActionItem(task, owners[0] if owners else None, due, owners)`: an item with no recognised owner is still appended, with `owner` `None` and `owners` empty. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (a rejected date and one never given are both `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` remains, so the gap is as it was. |
| C6 | held | `- if (_key(task), owner) in seen:` / `+ if (_key(task), owners) in seen:`: still a code comparison regardless of case and spacing, now on the tuple of owners. The tuple is ordered, so the same two owners in a different order would count as different. |
| C7 | held | not touched |
| C8 | held | Still one `model(prompt)` call with no retry; the added prompt text keeps several names "still on the same line" in the `task \| owner \| due` form. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
