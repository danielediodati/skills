## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ body=_without_quotes(body)[:MAX_BODY_CHARS]` with `+QUOTED = re.compile(r"^\s*>")`: a pattern match, not the model, decides which text counts as what the customer needs. A `>` line the new text depends on never reaches the model. |
| F2 | moved toward code | `+ drop = [bool(QUOTED.match(line)) for line in lines]`: the criterion "earlier messages do not count" is applied as a code rule. The line says criteria go in the prompt, not in code. |
| F3 | moved toward code | `+ return "\n".join(line for line, d in zip(lines, drop) if not d).strip()`: code fixes that quoted text can never inform the summary. The model cannot weigh it. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults are left as they were, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS]` / `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: the line allows the body to be cut only to a fixed cap. Code now also removes lines by pattern, so the call no longer sees the ticket. |
| C8 | held | not touched; the `ValueError` check still runs on the raw subject and body before the model is called. |
| B1 | held | Still one call, and `[:MAX_BODY_CHARS]` is still applied to the body that is sent. |

## Trial

- where: code
- flagged: no
- stopped: no
