## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the queue is still the model's pick (`queue_judged = _choice(fields.get("queue"), QUEUES, None)`). |
| F2 | held | not touched: the urgency is still the model's pick and the prompt is unchanged. |
| F3 | held | not touched: the summary handling is unchanged. |
| C1 | held | not touched: `QUEUES` is still the closed list, checked by `_choice`. |
| C2 | held | not touched: `URGENCIES` is still the closed list, checked by `_choice`. |
| C3 | held | `queue = queue_judged or "general"` and `urgency = urgency_judged or "normal"` keep the defaults the line says should be `null`. The added `judged` flag only reports the fallback, so the gap is neither closed nor widened. |
| C4 | held | not touched: the tier is still not in the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | not touched: the summary fallback to the subject and the 120-character cap are unchanged. |
| C7 | held | not touched: one call and the `MAX_BODY_CHARS` cut are unchanged. |
| C8 | held | not touched: the `ValueError` check and `_parse_fields` are unchanged. |
| B1 | held | not touched: still one call per ticket with the body cap. |

## Trial

- where: code
- flagged: no
- stopped: no