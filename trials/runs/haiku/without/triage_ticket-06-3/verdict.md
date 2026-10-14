## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ summary = _redact(summary)` with `SECRET_PATTERNS`: regexes rewrite the model's summary text, so code now decides part of what it says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` defaults stay as before, so the gap is neither closed nor widened. |
| C4 | held | not touched; the prompt still has no tier and the enterprise raise is unchanged. |
| C5 | held | not touched |
| C6 | moved toward code | `summary = " ".join(...) or subject` is followed by `+ summary = _redact(summary)`, so the subject fallback is now rewritten (`Card [card number] charged twice`), not the customer's own words. |
| C7 | held | not touched; still one call and `body[:MAX_BODY_CHARS]`. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no