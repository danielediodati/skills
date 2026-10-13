## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ When the notes make clear which person present took the item, write that person's name exactly as it appears in the list`: the model still reads who took it; the attendee-only gap in code is left as it was, neither closed nor widened. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (both set to `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched; still one model call. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
