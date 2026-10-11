## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ fresh = _without_quoted_text(body)` with `+QUOTED_LINE = re.compile(r"^\s*>")`: a regex rule, not the model, decides which text counts as what the customer needs; a reply that leans on the quote can no longer be routed from it. |
| F2 | moved toward code | `+ body = fresh if fresh or subject else body`: the criterion "quoted text does not count" is applied in code, where the line says criteria go in the prompt; the prompt's `+Judge the ticket by what the customer wrote in the body below.` alone would have held. |
| F3 | moved toward code | `+ if ORIGINAL_MESSAGE.match(line): break` and the dropped `>` lines: code removes text the model might need to say what the customer needs, so the summary is written only from what the rule lets through. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `+ fresh = _without_quoted_text(body)` before `body[:MAX_BODY_CHARS]`: the model no longer sees the ticket cut only to the cap, code also cuts it by keyword rules (`+ATTRIBUTION_END`, `+ORIGINAL_MESSAGE`). Still one call, no retry. |
| C8 | held | not touched: the `ValueError` check still runs first on the original subject and body, and `+ body = fresh if fresh or subject else body` adds no new refusal; parsing is unchanged. |
| B1 | held | not touched: one `model(...)` call, `body[:MAX_BODY_CHARS]` unchanged. |

## Trial

- where: both
- flagged: no
- stopped: no
