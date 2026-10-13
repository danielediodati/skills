## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be a complete sentence of at most {max_chars} characters.` sets form, not content; the model still writes the reason and the rewrite. Code's shortening is judged under C5. |
| F5 | held | not touched: `SHORTEN_PROMPT` names no language, so the model still chooses it. |
| C1 | held | not touched: the first call still lists every in-stock product. |
| C2 | held | `+ for product_id, reason in _parse(answer):` is a refactor; the `not in available or product_id in seen` check and the `limit` break are unchanged. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` becomes `+ new = _shorten_locally(p["reason"])`, which can `return ""`. Code now cuts to a sentence or clause boundary, or drops a written reason, tighter than "cut to 80 characters". |
| C6 | moved toward the model | `+ rewritten = dict(_parse(model(SHORTEN_PROMPT.format(`: a second model call where the line allows one, with no retry. |
| C7 | held | `LIST_MARKER.sub("", line).partition("|")` moved into `_parse` unchanged; the blank-search, nothing-in-stock and `limit < 1` paths are not touched. |
| B1 | moved toward the model | `+ if too_long: rewritten = dict(_parse(model(SHORTEN_PROMPT.format(`: up to two calls per search, and the line does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no
