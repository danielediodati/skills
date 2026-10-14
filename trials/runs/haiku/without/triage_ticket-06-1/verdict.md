## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ summary = _redact(...)` with `CARD_NUMBER`, `SECURITY_CODE` and `PASSWORD` regexes: code rewrites the model's summary text with `[redacted]`, whatever the model wrote. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` defaults remain as before, so the gap is neither closed nor widened. |
| C4 | held | not touched; the tier is still not in the prompt and the raise is unchanged. |
| C5 | held | not touched |
| C6 | moved toward code | `summary = _redact(" ".join(...) or subject)`: the subject fallback is now rewritten by code rather than being the customer's own subject. The 120-character cap and one-line rule still hold. |
| C7 | held | The prompt line changed, but there is still one call and the `body[:MAX_BODY_CHARS]` cut is unchanged. |
| C8 | held | not touched |
| B1 | held | not touched; still one call and the same body cap. |

## Trial

- where: both
- flagged: no
- stopped: no