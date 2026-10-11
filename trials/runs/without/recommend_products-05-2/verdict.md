## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be one complete sentence of at most {max_chars} characters.` is a general rule on form taken from the request; the model still decides what each reason says. The shortening is judged under C5. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | The loop now reads `+ for product_id, reason in _parse(answer):`, but `if product_id not in available or product_id in seen` and the `limit` break are unchanged. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward the model | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` is replaced by `+ answer = model(REWRITE_PROMPT.format(`: the model now does the fitting the line gives to code. The fallback `re.match(r"(.*[.!?])(?:\s|$)", text[:MAX_REASON_CHARS + 1])` can return 81 characters, and elsewhere blanks a non-empty reason. |
| C6 | moved toward the model | `+ answer = model(REWRITE_PROMPT.format(` in `_shorten_reasons`: a second model call to redo over-long reasons, where the line allows one call and no retry. |
| C7 | held | `_parse` keeps `LIST_MARKER.sub("", line).partition("|")`; the blank-search, nothing-in-stock and `limit < 1` paths are not touched. |
| B1 | moved toward the model | `+ _shorten_reasons(picks, model)` makes up to two model calls per search; the line sets one and does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no
