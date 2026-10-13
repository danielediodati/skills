## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ so write it as one complete sentence that fits within {max_reason} characters.`: tells the model the space it has; what the reason says is still the model's. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+ max_reason=MAX_REASON_CHARS,` only feeds the prompt; the cut `[:MAX_REASON_CHARS]` and the kept empty reason are unchanged. |
| C6 | held | not touched; the agent named a second call as an option and did not add it. |
| C7 | held | not touched |
| B1 | held | not touched; still one `model(...)` call. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
