## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if QUOTED.match(line): continue` and `+ if ORIGINAL_MARKER.match(line): break`: regex rules, not the model, decide which part of the ticket counts. A reply like "still not working" loses the context the model needs to pick the queue. |
| F2 | moved toward code | `+ body = _strip_quoted(ticket.get("body", ""))`: the criterion "quoted history does not count" is applied in code, where the line says criteria go in the prompt. The model cannot weigh the earlier exchange at all. |
| F3 | moved toward code | `+ body = _strip_quoted(ticket.get("body", ""))`: code fixes what the summary can be about by removing quoted lines and everything after a separator. The model summarises only what the regexes let through. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `+ kept = [] ... if ORIGINAL_MARKER.match(line): break`: the line lets code cut the body only at a fixed cap, and code now also removes content by pattern before `body[:MAX_BODY_CHARS]`. Still one call, no chunking, no retry. |
| C8 | moved toward code | `+ body = _strip_quoted(ticket.get("body", ""))` runs before `if not subject and not body`: a ticket that has a body, all of it quoted, and no subject now raises `ValueError`. Answer parsing is not touched. |
| B1 | held | not touched: one model call, `body[:MAX_BODY_CHARS]` unchanged. |

## Trial

- where: code
- flagged: no
- stopped: no
