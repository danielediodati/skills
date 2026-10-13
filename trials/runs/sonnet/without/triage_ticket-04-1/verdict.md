## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ kept = [line for line in body.splitlines() if not line.lstrip().startswith(">")]`: a code rule decides quoted text is not the request and removes it, so on an inline reply or a "see below" the model lacks what it needs to route. The prompt text "route and summarise on what the customer is asking for now" is only a criterion. |
| F2 | moved toward code | `+ body=_fit(_drop_quoted(body), MAX_BODY_CHARS)`: the same rule withholds quoted lines from the urgency judgement, even on bodies under the cap. |
| F3 | moved toward code | `+ def _drop_quoted(body):` "Remove lines an email client quoted": code decides what the summary cannot be about, and the model cannot weigh the quoted text as the prompt's "context". |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `+ body=_fit(_drop_quoted(body), MAX_BODY_CHARS)`: the line has the model see the ticket cut only to a cap, and code now also filters it by content. `+MAX_BODY_CHARS = 12000` is the budget number and `_fit` is still one cut to a fixed cap, with no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `-MAX_BODY_CHARS = 2000` / `+MAX_BODY_CHARS = 12000`: a budget number raised; still one model call, with the body cut to the cap. |

## Trial

- where: both
- flagged: no
- stopped: no
