## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if not QUOTE_LINE.match(line) and not ATTRIBUTION.match(line)`: a regex, not the model, decides which text counts as what the customer needs; no line allows this cut. The prompt note alone would hold. |
| F2 | moved toward code | `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: "quoted lines do not count" is a criterion placed in code, where the line says criteria go in the prompt. |
| F3 | moved toward code | `+ QUOTE_LINE = re.compile(r"^\s*>")`: code removes text the summary could draw on, so a reply that only makes sense with its quote ("> did the refund arrive?" / "No.") is summarised blind. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults are as before, so the gap is unchanged. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS]` / `+ body=_without_quotes(body)[:MAX_BODY_CHARS]`: the line lets code cut the body to the cap only; code now also filters lines out. Still one call, cap unchanged. |
| C8 | held | not touched |
| B1 | held | not touched: still one call, and `[:MAX_BODY_CHARS]` still applies the 2000 cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
