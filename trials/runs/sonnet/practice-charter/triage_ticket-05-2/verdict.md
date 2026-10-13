## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary is used as before; `fallback.append("summary")` only records when it gave none. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES, None)` still checks against the same closed list; the output is still one of the five queues. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES, None)` still checks against the same closed list; the output is still one of the four levels. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"` / `+ fallback.append("queue")` and `+ "judged": not fallback`: the default stays instead of `null`, but an unclassified field no longer shows as decided. Gap closed in part. |
| C4 | held | not touched: the tier is still absent from the prompt and the `enterprise` raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged; the `null` case still depends on the C3 gap, which the change did not widen. |
| C6 | held | `+ if not summary: summary = subject`: same fallback to the subject as `or subject` before; the one-line and 120-character cap are unchanged. |
| C7 | held | not touched: one model call, body cut at `MAX_BODY_CHARS`, no retry or chunking. |
| C8 | held | not touched: the `ValueError`, `FIELD` and `_parse_fields` are unchanged; `# default may be None` is only a comment on `_choice`. |
| B1 | held | not touched: one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
