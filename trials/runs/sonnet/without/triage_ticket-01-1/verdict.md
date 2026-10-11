## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ body = _strip_quoted(body)`: regex rules now decide which text counts as the customer's need. `+ if SEPARATOR.match(line): break` can drop the very message the model must read (a forward, an inline reply). |
| F2 | moved toward code | `+ if QUOTED.match(line): continue`: the criterion "quoted text does not count" is applied as a code rule, where the line says criteria go in the prompt, not in code. |
| F3 | moved toward code | `+ text = ATTRIBUTION.sub("", text)` and the `>`/separator rules: code fixes what the summary may be about by removing text before the model sees it. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `+ body = _strip_quoted(body)`: the model no longer sees the ticket cut only at the cap; keyword rules remove more than the line allows. Still one call, no retry. |
| C8 | held | not touched: the strip is added after `raise ValueError(...)`, and the answer parsing is unchanged. |
| B1 | held | not touched: one `model(...)` call, `body[:MAX_BODY_CHARS]` unchanged. |

## Trial

- where: code
- flagged: no
- stopped: no
