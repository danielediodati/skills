## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged, and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary is used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: still checked against the same closed list. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: still checked against the same closed list. |
| C3 | moved toward the charter | `+ return value if value in allowed else None` and `+ fallback.append("queue")`: an invalid field is now marked as unclassified. Partial only, since `+ queue = "general"` and `+ urgency = "normal"` still put the defaults. |
| C4 | held | not touched: the tier stays out of the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged, and urgency is still never `null` at that point, as before. |
| C6 | held | `+ if not summary: summary = subject`: same subject fallback and 120 cap; `+ fallback.append("summary")` only reports it. |
| C7 | held | not touched: one call, body cut at `MAX_BODY_CHARS`, no retry or chunking. |
| C8 | held | not touched: the `ValueError`, `FIELD` parsing, first-occurrence rule and the normalization in `_choice` are unchanged. |
| B1 | held | not touched: one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
