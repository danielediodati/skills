## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (code keeps only attendee names) is as before. |
| F4 | held | not touched |
| C1 | held | not touched; items without owner or due are still kept. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; code still sets both cases to `None`. |
| C4 | held | not touched |
| C5 | held | `return items[:MAX_ITEMS], max(0, len(items) - MAX_ITEMS)`: the cap of 10 stays, and the count only reports the cut, so the gap is neither closed nor widened. |
| C6 | held | not touched |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | `items, _ = extract_with_overflow(...)`: one call, no retry; blank notes still return without calling the model. |
| B1 | held | not touched; still one model call per set of notes. |

## Trial

- where: code
- flagged: yes
- stopped: no