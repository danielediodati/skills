## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Judge only what the customer wrote this time, wherever the` / `+ quoted messages sit.`: a criterion that informs the model's reading; no queue is dictated. |
| F2 | held | `+ The quoted conversation is not a request.`: a criterion in the prompt, where the line says criteria go; the model still picks the level. |
| F3 | held | `+ Judge only what the customer wrote this time`: tells the model what to read, not what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `general` and `normal` are still the defaults, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched: still one call, with `body[:MAX_BODY_CHARS]` unchanged; the added test only reads the prompt. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
