## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Judge only what the customer wrote this time, wherever the quoted messages sit.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | `+ Judge only what the customer wrote this time`: criteria in the prompt, not in code, as the line allows; no level is fixed. |
| F3 | held | `+ The quoted conversation is not a request.`: says what to read, not what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched: still one call, with `body[:MAX_BODY_CHARS]` at 2000; the stripping step was proposed, not made. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
