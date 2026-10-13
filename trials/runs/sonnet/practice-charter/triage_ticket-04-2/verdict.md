## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Route and summarise on what the customer is asking for, wherever in the message they say it.`: a criterion that informs the model's reading; it still picks the queue. |
| F2 | held | not touched |
| F3 | held | `+Route and summarise on what the customer is asking for, wherever in the message`: guidance on what to look at; the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched; the added prompt text leaves the single call and `body[:MAX_BODY_CHARS]` as they were. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
