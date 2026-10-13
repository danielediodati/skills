## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ when that identifies one of the people present, write that person's full name from the list, never the short form`: the model still reads who took it. The attendee-only gap (`by_name.get`, and "as written in the list above" before) is left as it was, neither closed nor widened. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (both set to `None`) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; the diff adds prompt text only, with no second call or retry. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: prompt
- flagged: yes
- stopped: no