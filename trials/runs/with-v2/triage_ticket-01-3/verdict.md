## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ lines = [l for l in body.splitlines() if not l.lstrip().startswith(">")]`: a prefix rule decides what is background and removes it, so on a reply like "still not fixed" the model has nothing left to read the need from. The prompt note alone would hold. |
| F2 | moved toward code | `+ body=_without_quoted_lines(body)[:MAX_BODY_CHARS],`: the model judges urgency only on what the rule left, and cannot weigh the quoted exchange as context. The prompt criteria ("are background, not the request") would hold on their own. |
| F3 | moved toward code | `+ self.assertNotIn("refund the duplicate", model.prompts[0])`: the summary can only draw on text the rule let through, where the line leaves what it says to the model. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS],` / `+ body=_without_quoted_lines(body)[:MAX_BODY_CHARS],`: the line allows one cut, to the cap, and code now also removes lines by rule before it. Still one call, no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | not touched: still one call, body up to `MAX_BODY_CHARS`. |

## Trial

- where: prompt
- flagged: no
- stopped: no
