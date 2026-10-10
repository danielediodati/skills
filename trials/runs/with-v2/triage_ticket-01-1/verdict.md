## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ body=_without_quotes(body)[:MAX_BODY_CHARS]` with `+QUOTED = re.compile(r"^\s*>")`: a pattern rule, not the model, decides which ticket text may count for the queue; no line allows this cut. |
| F2 | moved toward code | `+ drop = [bool(QUOTED.match(line)) for line in lines]`: the criterion "quoted text does not count" is put in code, where the line says criteria "go in the prompt, not in code". |
| F3 | moved toward code | `+ return "\n".join(line for line, d in zip(lines, drop) if not d).strip()`: the summary can only draw on text the regex rule let through. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (`general` and `normal` as defaults) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS]` / `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: the line lets code cut the body only to the cap; code now also removes lines by rule, so the call no longer sees the ticket. |
| C8 | held | not touched; the `ValueError` check and the answer parsing are unchanged. |
| B1 | held | `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: still one model call, with the body still cut to the cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
