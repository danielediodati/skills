## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (non-attendee owner set to `None`) is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched; no owner or due check was added, and the items cut are still cut by the existing cap alone. |
| C2 | held | not touched |
| C3 | held | not touched; a rejected date and a missing one are both still `None`. |
| C4 | held | not touched |
| C5 | held | `+ dropped = items[MAX_ITEMS:]` / `+ on_dropped(dropped)` only reports the cut; `return items[:MAX_ITEMS]` is unchanged, so the gap of 10 is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched; `+ dropped = items[MAX_ITEMS:]` is taken after the existing sort and does not change the order. |
| C8 | held | not touched; `on_dropped` is a caller callback, not a second model call, and the skipping of malformed lines and `NONE` are unchanged. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: partial
