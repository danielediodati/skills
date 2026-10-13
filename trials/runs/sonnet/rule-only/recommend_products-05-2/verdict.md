## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be a complete sentence or thought of at most {max_chars} characters,` informs form and length; the model still chooses what the reason says. The blanking is judged under C5. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` replaced by `+ if len(reason) > MAX_REASON_CHARS:` `+ reason = ""`: the line says cut to 80; code now discards the whole reason, a new rule made on purpose. |
| C6 | held | not touched: still one `model(...)` call; a retry is only offered in the final answer, not made. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per search. |

## Trial

- where: both
- flagged: yes
- stopped: no
