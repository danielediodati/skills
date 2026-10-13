## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Read the whole message and triage what the customer is asking for now, not what the thread started as`: a criterion that informs the model's reading; the queue is still its choice. |
| F2 | held | Same added prompt paragraph: it sets no urgency level and no rule mapping content to a level; the judgement stays the model's. |
| F3 | held | Same added prompt paragraph: it says what to summarise from, not what the summary says; the model still writes it. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults remain as before, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `-MAX_BODY_CHARS = 2000` / `+MAX_BODY_CHARS = 20000`: the cap is a budget number that may be raised; still one call, a fixed cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+MAX_BODY_CHARS = 20000`: still one model call per ticket, with the body cut at the cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
