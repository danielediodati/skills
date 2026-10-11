## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ body=_without_quoted_lines(body)[:MAX_BODY_CHARS]`: code removes every `>` line, so a reply like "still not fixed" loses the thread the model needs to pick the queue. The prompt text alone ("are background, not the request") is a criterion. |
| F2 | moved toward code | `+ lines = [l for l in body.splitlines() if not l.lstrip().startswith(">")]`: a prefix rule in code settles what may weigh on urgency, where the line says criteria "go in the prompt, not in code". |
| F3 | moved toward code | `+ body=_without_quoted_lines(body)[:MAX_BODY_CHARS]`: the model summarises only what code left in; quoted context it could use to say what the customer needs is cut by rule. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults stay as they were, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS]` `+ body=_without_quoted_lines(body)[:MAX_BODY_CHARS]`: the line has the call see the ticket with its body cut only to the cap; code now also filters lines out. Still one call, no retry. |
| C8 | held | not touched |
| B1 | held | not touched: still one model call, body up to the 2000 cap. |

## Trial

- where: both
- flagged: no
- stopped: no
