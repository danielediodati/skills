## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if PRICE_RATING_OR_RANK.search(reason): reason = ""` and `+Do not mention a price, a rating, or how a product ranks...`: code now vetoes reasons by keyword and digit where the line says claims are not checked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `reason = " ".join(reason.split())[:MAX_REASON_CHARS]` is kept, and an empty reason is still kept; the new blanking is a content veto, counted under F4. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no