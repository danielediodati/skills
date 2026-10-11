## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ kept = [line for line in body.splitlines() if not line.lstrip().startswith(">")]`: a code rule decides quoted text is irrelevant to the need, so a reply like "still not fixed, see below" reaches the model without its subject. The added prompt text ("route and summarise on what the customer is asking for now") is only a criterion. |
| F2 | moved toward code | `+ body=_fit(_drop_quoted(body), MAX_BODY_CHARS)`: the model judges urgency on a body from which code has removed every `>` line, whatever those lines said. |
| F3 | moved toward code | `+ def _drop_quoted(body):` `"""Remove lines an email client quoted (">"), unless nothing else is left."""`: code fixes what the summary cannot be about before the model reads it. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `+ body=_fit(_drop_quoted(body), MAX_BODY_CHARS)`: the line allows the body cut to a cap, not filtered by a rule on its content. `MAX_BODY_CHARS = 12000` is the budget number and the middle cut in `_fit` is still one cut to a fixed cap, with one call and no retry. |
| C8 | held | not touched |

## Trial

- where: prompt
- flagged: no
- stopped: no
