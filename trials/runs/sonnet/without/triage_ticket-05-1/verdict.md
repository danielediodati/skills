## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and a valid queue from the model still passes through as given. |
| F2 | held | not touched: no criteria or rule added, and a valid urgency from the model is still used as given. |
| F3 | held | not touched: the model's summary text is used as before, and `defaulted` only reports when it was empty. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | held | `+ queue = queue or "general"` / `+ urgency = urgency or "normal"`: the defaults are still output where the line says `null`. `defaulted` and `needs_review` sit beside them, so the gap is as it was. |
| C4 | held | not touched: the prompt still omits the tier, and the `enterprise` raise in code is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and the `null` case stays unimplemented, as inherited with C3. |
| C6 | held | `+ summary = summary or subject` with `summary[:MAX_SUMMARY_CHARS]` kept: same one-line, 120-character cap and subject fallback, only reordered. |
| C7 | held | not touched: one `model(...)` call, `body[:MAX_BODY_CHARS]`, no retry or chunking added. |
| C8 | held | not touched: the `ValueError`, `FIELD`, `_parse_fields` and the cleaning in `_choice` are unchanged; only the `default` argument was replaced by `None`. |
| B1 | held | not touched: still one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
