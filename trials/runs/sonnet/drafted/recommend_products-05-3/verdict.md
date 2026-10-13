## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ must be a complete thought that fits in it: write it short enough to finish, never trailing off.`: tells the model the space it has; what the reason says is still the model's. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+ max_reason=MAX_REASON_CHARS,` only passes the limit to the prompt; the cut `[:MAX_REASON_CHARS]` and the kept empty reason are unchanged. |
| C6 | held | not touched; still one `model(...)` call, no retry added. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial