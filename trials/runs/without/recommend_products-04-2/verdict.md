## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if _states_price_or_rating(reason): reason = ""` and `+ Do not mention prices, ratings, or how products compare on price or rating`: a keyword match overrides the model's reason, where the line says claims are not checked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+ reason = " ".join(reason.split())` and `+ "reason": reason[:MAX_REASON_CHARS]`: still one line, cut to 80, and an empty reason is kept. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
