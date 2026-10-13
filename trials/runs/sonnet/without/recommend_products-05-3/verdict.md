## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be one complete sentence of at most {max_chars} characters.` sets form and length only; the model still decides what the reason says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | `+ for product_id, reason in _parse(answer, available):` moves the same real, in-stock, once-only check into a helper; `if len(picks) == limit: break` is kept. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` replaced by `_fit` and `+ pick["reason"] = fitted[pick["id"]] or ""`: a sentence-end rule, and a model-written reason blanked where the line says cut to 80. |
| C6 | moved toward the model | `+ retry = model(SHORTEN_PROMPT.format(`: a second model call to rewrite reasons, where the line allows one call and no retry. |
| C7 | held | Blank search, nothing in stock and `limit < 1` are not touched; `LIST_MARKER.sub("", line).partition("|")` is moved unchanged into `_parse`. |
| B1 | moved toward the model | `+ if too_long: retry = model(SHORTEN_PROMPT.format(`: up to two model calls per search, and the line does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no
