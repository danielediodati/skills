## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if not 0 < len(new) <= MAX_REASON_CHARS: new = _shorten_locally(p["reason"])` with `+ return ""`: a punctuation rule picks which part of the reason survives, or blanks it. The prompt's `+ Each reason must be a complete sentence of at most {max_chars} characters.` is only a general rule. |
| F5 | held | not touched: `addressed to the customer` stays in the prompt, and `SHORTEN_PROMPT` fixes no language. |
| C1 | held | not touched |
| C2 | held | The id check is unchanged behind `+ for product_id, reason in _parse(answer):`. The rewrite is read only by `rewritten.get(p["id"], "")` for picks already validated. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward the model | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` becomes `+ "reason": reason,` plus `+ SHORTEN_PROMPT`: the model now does the shortening the line gives to a code cut. Code still enforces one line and 80 characters. |
| C6 | moved toward the model | `+ rewritten = dict(_parse(model(SHORTEN_PROMPT.format(` : a second model call where the line says one call, no retry. |
| C7 | held | `+ def _parse(answer):` keeps `LIST_MARKER.sub("", line).partition("|")`, so markers and chatter are still skipped. The blank-search, nothing-in-stock and `limit` guards are not touched. |
| B1 | moved toward the model | `+ if too_long: rewritten = dict(_parse(model(SHORTEN_PROMPT.format(` : up to two calls per search, and the line does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no
