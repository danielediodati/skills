## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The reason must be a complete sentence of at most {max_chars} characters, including spaces`: fixes form and length, which C5 already bounds; the model still decides what the reason says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+        max_chars=MAX_REASON_CHARS,` only tells the model the cap; the code cut `[:MAX_REASON_CHARS]` and the kept empty reason are unchanged. |
| C6 | held | not touched; the answer names a retry as an option and leaves it out. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
