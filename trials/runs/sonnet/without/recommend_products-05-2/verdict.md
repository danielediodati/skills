## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be one complete sentence of at most {max_chars} characters.` and `keeps its main point` set length and form; the model still chooses what the reason says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | `+ for product_id, reason in _parse(answer):` only moves the parsing; the `not in available or product_id in seen` check and the `limit` break are unchanged. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward the model | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` replaced by `+ answer = model(REWRITE_PROMPT.format(`: the model now does the shortening, with a code fallback to a sentence or `""`. `text[:MAX_REASON_CHARS + 1]` can also return 81 characters. |
| C6 | moved toward the model | `+ _shorten_reasons(picks, model)` with `+ answer = model(REWRITE_PROMPT.format(`: a second model call where the line allows one. |
| C7 | held | `+def _parse(answer):` keeps `LIST_MARKER.sub("", line).partition("|")`; the blank-search, nothing-in-stock and `limit` checks are not touched. |
| B1 | moved toward the model | `+ answer = model(REWRITE_PROMPT.format(`: up to two model calls per search against a budget of one. |

## Trial

- where: both
- flagged: no
- stopped: no
