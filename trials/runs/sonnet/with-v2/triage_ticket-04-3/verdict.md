## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ The customer's actual request can be anywhere in the message`: informs the reading without fixing a queue; the model still decides. |
| F2 | held | not touched; the added prompt text sets no urgency level or criterion. |
| F3 | held | `+ Read the whole message before deciding; the subject may describe an older thread.`: informs what to summarise; the wording stays the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (`general` and `normal` defaults) is left as it was. |
| C4 | held | not touched; the tier still does not reach the prompt and code still raises `enterprise` one level. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- MAX_BODY_CHARS = 2000` / `+ MAX_BODY_CHARS = 20000`: a budget number the line says may be raised; still one call, a fixed cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+ MAX_BODY_CHARS = 20000`: the cap is raised, still one model call per ticket with the body up to the cap. |

## Trial

- where: both
- flagged: yes
- stopped: no
