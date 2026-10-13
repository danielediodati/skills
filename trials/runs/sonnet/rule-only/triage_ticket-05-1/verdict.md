## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary is still used whenever it gives one. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ queue = "general"` / `+ fallbacks.append("queue")`: the default is still written rather than `null`, but it no longer shows as decided, so the gap closes in part. |
| C4 | held | not touched: the tier is still absent from the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged, and urgency is still never `null`, as before. |
| C6 | held | `+ if not summary: summary = subject`: same subject fallback, now also recorded, and the one-line 120-character cap is unchanged. |
| C7 | held | not touched: one model call, body cut at `MAX_BODY_CHARS`, no retry or chunking. |
| C8 | held | not touched: the `ValueError`, `FIELD` parsing and first-occurrence rule are unchanged, and `_choice` strips and lowercases as before. |
| B1 | held | not touched: one call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
