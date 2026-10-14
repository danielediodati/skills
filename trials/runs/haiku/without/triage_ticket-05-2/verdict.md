## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched; the prompt and the model's queue choice are unchanged. |
| F2 | held | not touched; no urgency criteria were added to the prompt or code. |
| F3 | held | not touched; the summary still comes from the model's `summary` field. |
| C1 | held | `_choice(fields.get("queue"), QUEUES)` still accepts only the five queues; anything else is treated as unusable. |
| C2 | held | `_choice(fields.get("urgency"), URGENCIES)` still accepts only the four levels. |
| C3 | held | `queue = "general"` and `urgency = "normal"` are still set when the choice is `None`. The new `fallbacks` and `needs_review` keys flag the defaults but do not make the values `null`, so the gap stays as it was. |
| C4 | held | the enterprise `level = min(URGENCIES.index(urgency) + 1, ...)` block is untouched and the tier still does not reach the prompt. |
| C5 | held | `RESPOND_WITHIN_HOURS[urgency]` is unchanged; a default urgency still yields 24, which is the existing gap, not a new one. |
| C6 | held | `if not summary: ... summary = subject` and `summary[:MAX_SUMMARY_CHARS]` give the same result as before. |
| C7 | held | not touched; still one call with `body[:MAX_BODY_CHARS]`, with no retry or merge. |
| C8 | held | not touched; the empty-ticket `ValueError` and `_parse_fields` are unchanged. |
| B1 | held | not touched; one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: yes
- stopped: no