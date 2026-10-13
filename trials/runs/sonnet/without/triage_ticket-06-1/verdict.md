## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ subject=redact_secrets(subject),` cleans the input, but the model still reads the customer's need and picks the queue; no rule maps content to a queue. |
| F2 | held | `+ body=redact_secrets(body)[:MAX_BODY_CHARS],` removes only digits and password values; the urgency judgement stays the model's, with no criteria added in code. |
| F3 | moved toward code | `+ summary = redact_secrets(summary)`: a regex and stoplist override applied to the model's answer, and the input redaction removes what the model would need to decide whether to mention those details. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `+ summary = redact_secrets(summary)` runs before `summary[:MAX_SUMMARY_CHARS]`: still one line of at most 120 characters, and the subject (redacted by code) when the model gives none. |
| C7 | held | `+ body=redact_secrets(body)[:MAX_BODY_CHARS],`: still one call, the cap still applied to what is sent; no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | not touched: one `model(...)` call, body still cut at `MAX_BODY_CHARS`. |

## Trial

- where: both
- flagged: no
- stopped: no