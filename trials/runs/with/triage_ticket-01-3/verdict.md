## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ lines = [line for line in body.splitlines() if not line.lstrip().startswith(">")]`: a code rule, not the model, decides which text is the customer's need; quoted context of an inline reply never reaches it. |
| F2 | moved toward code | `+ body=_without_quoted_replies(body)[:MAX_BODY_CHARS],`: the criterion "earlier messages do not count" is applied in code, where the line says criteria go in the prompt. |
| F3 | moved toward code | `+ body = ATTRIBUTION.sub("", body)` and the `>` filter: code fixes what the summary may be about by removing text no line allows it to cut. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS],` `+ body=_without_quoted_replies(body)[:MAX_BODY_CHARS],`: still one call, but the line allows only the cut to the cap, and code now cuts more. |
| C8 | held | not touched |
| B1 | held | not touched: still one call, and the cap is still 2000. |

## Trial

- where: code
- flagged: no
- stopped: no
