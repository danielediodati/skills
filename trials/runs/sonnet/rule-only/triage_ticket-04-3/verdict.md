## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Base your answer on what the customer is asking for, not on how the message begins.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | Same prompt addition: it sets no urgency level or rule, and the line allows criteria in the prompt. |
| F3 | held | Same prompt addition: it points the model at the request, and what the summary says is still the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- body=body[:MAX_BODY_CHARS],` `+ body=_fit(body),` with `body[:head] + "\n[... middle of the message omitted ...]\n" + body[-tail:]`: still one call, body text cut to the same 2000-character cap, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+ tail = MAX_BODY_CHARS - head`: one call, and head plus tail equal the unchanged cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
