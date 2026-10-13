## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: no urgency criteria or rules added in code or prompt. |
| F3 | held | not touched: the summary text is still the model's; `+ fallbacks.append("summary")` only records when the subject was used. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | held | `+ if queue is None: queue = "general"` and `+ urgency = "normal"`: the fields still carry defaults, not `null`. The gap is left as it was, with `fallbacks` reporting it beside the fields. |
| C4 | held | not touched: the tier is still absent from the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged, and urgency is still never `null` in the output. |
| C6 | held | `+ if not summary: summary = subject`: same subject fallback, and `summary[:MAX_SUMMARY_CHARS]` is unchanged. |
| C7 | held | not touched: one call, `body[:MAX_BODY_CHARS]`, no retry or chunking. |
| C8 | held | not touched: the `ValueError`, `FIELD` and `_parse_fields` are unchanged, and `_choice` normalizes as before, returning `None` instead of a default. |
| B1 | held | not touched: still one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: yes
- stopped: no