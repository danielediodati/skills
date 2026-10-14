## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (non-attendee owners set to `None`) is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | `+ return items[:MAX_ITEMS], max(0, len(items) - MAX_ITEMS)`: the cap of 10 stays and only a count of dropped items is added, so the gap is neither closed nor widened. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | `+ return [], 0` in the new function, and `extract_action_items` unwraps it to `[]`: still one call, and empty notes still skip the model. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: partial