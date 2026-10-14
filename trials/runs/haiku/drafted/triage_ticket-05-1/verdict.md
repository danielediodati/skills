## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `queue = _choice(fields.get("queue"), QUEUES, "general")` is unchanged; the new `judged` flag only reads the queue, it does not alter it. |
| C2 | held | `urgency = _choice(fields.get("urgency"), URGENCIES, "normal")` is unchanged; the `_clean` helper is the same strip and lower as before. |
| C3 | held | The `general` and `normal` defaults remain; `+ "judged": judged` only reports them and does not null the fields, so the gap stays as it was. |
| C4 | held | not touched; the tier is still not in the prompt and the enterprise raise block is unchanged. |
| C5 | held | not touched; `RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | not touched; the `or subject` fallback and the `[:MAX_SUMMARY_CHARS]` cap are unchanged. |
| C7 | held | not touched; still one call with `body[:MAX_BODY_CHARS]`, no retry. |
| C8 | held | not touched; the empty-ticket `ValueError` and `_parse_fields` are unchanged. |
| B1 | held | not touched; one call per ticket, cap unchanged. |

## Trial

- where: code
- flagged: no
- stopped: no