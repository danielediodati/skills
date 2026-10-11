## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be one complete sentence of at most {max_chars} characters.` is a criterion of form; every word shown is still the model's. Code's cutting and blanking is judged under C5. |
| F5 | held | not touched: neither the added prompt sentence nor `SHORTEN_PROMPT` fixes a language. |
| C1 | held | not touched: the first call still lists every product in `available`. |
| C2 | held | The check moved unchanged into `_parse`: `+ if product_id not in allowed or product_id in seen:`; `if len(picks) == limit: break` is kept. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` became `+ return reason[:ends[-1]] if ends else None` and `+ pick["reason"] = fitted[pick["id"]] or ""`. Code now cuts shorter than 80 at a sentence end, or blanks a reason the model wrote. |
| C6 | moved toward the model | `+ retry = model(SHORTEN_PROMPT.format(`: a second model call where the line allows one and no retry. |
| C7 | held | Blank search, nothing in stock and `limit` checks not touched; `LIST_MARKER.sub("", line)` and the skipping of chatter are kept in `_parse`. |
| B1 | moved toward the model | `+ retry = model(SHORTEN_PROMPT.format(`: up to two calls per search, and the line does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no
