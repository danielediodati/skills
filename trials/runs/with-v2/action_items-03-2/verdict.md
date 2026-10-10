## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+ If several people took it together, give all their names separated by ";".` and `+ owners: Tuple[str, ...]`: several owners now survive, closing part of the gap. Non-attendees are still dropped (`name = by_name.get(_key(part))`), so the rest of the gap stays. |
| F4 | held | not touched |
| C1 | held | `+ items.append(ActionItem(task, owners, due))` with `owners` possibly `()`: an item with no owner still stays in the list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` remain, so the gap is as it was. |
| C6 | moved toward the model | `+ if (_key(task), owners) in seen:` where `owners` is a tuple in the order the model wrote the names. The same task for the same two owners in a different order is listed twice, so the model's ordering decides what counts as a duplicate. |
| C7 | held | not touched |
| C8 | held | not touched; still one call, and lines are still split as `task \| owner \| due`. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
