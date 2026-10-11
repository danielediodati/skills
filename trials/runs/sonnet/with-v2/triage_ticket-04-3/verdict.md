## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ The customer's actual request can be anywhere in the message: after a quoted earlier exchange, after a pasted log, or in the last paragraph.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | `+ Read the whole message before deciding; the subject may describe an older thread.`: a criterion in the prompt, as the line allows; no level is defined or fixed. |
| F3 | held | `+ Read the whole message before deciding`: says where to look, not what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (`general` and `normal` as defaults) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- MAX_BODY_CHARS = 2000` / `+ MAX_BODY_CHARS = 20000`: the cap is a budget number and may be raised; still one call, body still cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+ MAX_BODY_CHARS = 20000`: still one call per ticket, body up to the cap; only the budget number changed. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
