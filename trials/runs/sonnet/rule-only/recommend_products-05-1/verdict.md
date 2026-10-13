## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The reason must be one complete sentence of at most {max_reason_chars} characters`: fixes form and length, not what the reason says; the model still writes it. |
| F5 | held | not touched; the prompt still says only `addressed to the customer`, and the model picks the language. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- "reason": " ".join(reason.split())[:MAX_REASON_CHARS],` `+ "reason": fit_reason(reason),` with `return reason[:end]`: a sentence-boundary rule replaces the cut to 80, and blanks an overlong single-sentence reason. |
| C6 | held | not touched; still one `model(...)` call, and the re-ask is only offered in the answer, not made. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per search. |

## Trial

- where: both
- flagged: yes
- stopped: no
