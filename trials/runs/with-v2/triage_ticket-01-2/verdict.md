## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: code, not the model, rules quoted text out of the queue decision. A reply like "still not fixed" loses the thread it needs. |
| F2 | moved toward code | `+ if not QUOTE_LINE.match(line) and not ATTRIBUTION.match(line)`: a regex removes context the model may need to weigh urgency. The prompt note alone ("they are background only") would have held. |
| F3 | moved toward code | `+ return "\n".join(kept).strip() or body`: the summary can only draw on what the regex kept, so code fixes what it may be about. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults are left as they were, so the gap is unchanged. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: still one call, same 2000 cap, no chunking or retry. |
| C8 | held | not touched; the `or body` fallback keeps a quotes-only body non-empty, and the `ValueError` check still runs before the call. |
| B1 | held | not touched; one call per ticket, cap unchanged. |

## Trial

- where: both
- flagged: no
- stopped: no
