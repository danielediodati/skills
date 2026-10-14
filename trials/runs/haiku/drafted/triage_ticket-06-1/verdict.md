## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ summary: ... leave out card numbers, security codes, passwords and any other secret the customer typed.` is a criterion the model applies by reading each ticket. The wording of the summary stays the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` defaults gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched; the 120-character cap and subject fallback are unchanged, and no redaction code was added. |
| C7 | held | not touched; still one call, and the prompt change adds no retry. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial