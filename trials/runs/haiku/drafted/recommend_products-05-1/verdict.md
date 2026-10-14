## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ ID | one complete sentence addressed to the customer, at most {reason_chars} characters`: a length and form criterion that informs the model; it still writes what the reason says. |
| F5 | held | not touched; "addressed to the customer" is kept in the new prompt wording. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `[:MAX_REASON_CHARS]` cut and the empty-reason handling are unchanged; the prompt only asks the model to fit. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial