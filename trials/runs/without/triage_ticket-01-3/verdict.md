## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ fresh = _without_quoted_text(body)` with `+ QUOTED_LINE = re.compile(r"^\s*>")`: a pattern match, not the model, decides which text counts as what the customer needs, and the model never sees the rest. |
| F2 | moved toward code | `+ if ORIGINAL_MESSAGE.match(line): break` and the dropped `>` lines: code removes text the model would weigh for urgency. The line puts criteria in the prompt, not in code. |
| F3 | moved toward code | `+ body = fresh if fresh or subject else body`: the summary can only be written from what the regex rules kept, e.g. "Point one is wrong." without the point it answers. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `+ fresh = _without_quoted_text(body)` before `body[:MAX_BODY_CHARS]`: the model no longer sees the ticket cut only to the cap; code cuts it further than the line says. Still one call, no retry. |
| C8 | held | `+ body = fresh if fresh or subject else body` comes after the unchanged `raise ValueError(...)`; the parsing is not touched. |
| B1 | held | not touched: still one call and `body[:MAX_BODY_CHARS]` at 2000. |

## Trial

- where: both
- flagged: no
- stopped: no
