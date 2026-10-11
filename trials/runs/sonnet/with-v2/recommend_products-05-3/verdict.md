## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The reason must be a complete sentence of at most {max_chars} characters, including spaces`: a general requirement on form and length that the model applies itself; what the reason says is still its choice. |
| F5 | held | not touched; the added prompt line says nothing about language. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+        max_chars=MAX_REASON_CHARS,` only tells the model the limit; the code cut `[:MAX_REASON_CHARS]` and the kept empty reason are unchanged. |
| C6 | held | not touched; no retry added, and the answer names a retry only as an option it did not take. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
