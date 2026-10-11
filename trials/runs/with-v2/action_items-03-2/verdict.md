## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward the charter | `+  If several people took it together, give all their names separated by ";".` and `+    owners: Tuple[str, ...]`: several owners now survive. Part of the gap stays: `name = by_name.get(_key(part))` still drops non-attendees. |
| C1 | held | `+        items.append(ActionItem(task, owners, due))`: an item whose owners end up `()` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (rejected and never-given dates both `None`) is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` are as they were. |
| C6 | held | `+        if (_key(task), owners) in seen:`: still a code comparison on the case- and space-folded task and canonical attendee names. The tuple is order-sensitive, so the same pair in a different order is not merged. |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the `rsplit("|", 2)` form check and `NONE` handling are unchanged. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
