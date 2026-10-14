## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `one complete sentence of at most {reason_chars} characters` shapes the form of the reason. What it says is still the model's, and claims are still unchecked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS]` became `+ "reason": _complete_reason(reason)`, which cuts back to the last sentence end and returns `""` if none fits. The line says cut to 80 characters. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no