## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ summary = _redact(" ".join(fields.get("summary", "").split())) or _redact(subject)`: code now rewrites the content of the model's summary with regex placeholders (`[card number]`, `[code]`, `[password]`) and a password stop-word list. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` defaults are still there, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | moved toward code | `+ or _redact(subject)`: the fallback is no longer the customer's subject as written; code rewrites it. The 120-character cap is unchanged. |
| C7 | held | The prompt gains "Never repeat card numbers, security codes, passwords..." but it is still one call, the body cap is unchanged and there is no retry. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no