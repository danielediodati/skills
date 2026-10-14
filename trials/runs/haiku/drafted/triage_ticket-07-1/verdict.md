## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ urgent: something is broken for the customer right now...` and the other level definitions are criteria in the prompt that inform the model's judgement; the model still reads each ticket and picks the level, and the charter says criteria go in the prompt. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` defaults remain, so the gap the line marks as not yet in code is unchanged. |
| C4 | held | not touched; the enterprise raise stays in code and the prompt still has no tier. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial