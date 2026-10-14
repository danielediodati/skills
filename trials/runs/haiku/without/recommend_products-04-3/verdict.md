## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if CLAIM.search(reason): reason = ""` and the prompt line `+The reason must not mention any price, rating, or how a product ranks or compares with the others.`: code now blanks reasons by keyword, where the line says claims are not checked. |
| F5 | held | not touched: the filter blanks reasons but does not fix their language. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `"reason": reason[:MAX_REASON_CHARS]` still cuts to one line of 80 characters and an empty reason is kept. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no