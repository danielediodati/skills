## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt's queue instructions are unchanged and no rule was added. |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the "Not yet in code" gap (`general` and `normal` defaults) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `-MAX_BODY_CHARS = 2000` / `+MAX_BODY_CHARS = 12000`: the cap is a budget number the line says may be raised. Still one call, one fixed cut, no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | `+MAX_BODY_CHARS = 12000`: still one model call per ticket, with the body up to the (raised) cap. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
