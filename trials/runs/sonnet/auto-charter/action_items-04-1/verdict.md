## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ work out which person present it refers to and give that person's name from the list`: the model still reads who took it. The attendee-only gap was already in the prompt ("as written in the list above") and in code, and is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched; `+ Write "none" if nobody took it, or if you cannot tell which person it was` still keeps the item in the list. |
| C2 | held | not touched |
| C3 | held | not touched; the gap (both set to `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap (`MAX_ITEMS = 10`) is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and only the owner instruction in the prompt changed. |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
