## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If the notes say someone who was not present took it, write that person's name as the notes give it.` and `+ elsewhere = owner is None and _names_outsider(fields[1], attendees)`: a non-attendee owner now survives as a flag. The gap closes only in part, since the name itself is still set to `None`. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owner, due, elsewhere))`: an item with no owner or no due date is still appended. |
| C2 | held | not touched |
| C3 | held | not touched; a rejected due date and one never given are both still `None`, the gap as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` still caps at 10, the gap as it was. |
| C6 | held | not touched; the comparison is still `(_key(task), owner)`, as before the change. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with the same skipping of blank notes and malformed lines. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: both
- flagged: yes
- stopped: no