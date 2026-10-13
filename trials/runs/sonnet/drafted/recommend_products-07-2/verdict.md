## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Only pick a product if it genuinely suits what the customer searched for.`: a criterion that informs the model's judgement; the model still reads each search and decides what suits it. |
| F2 | held | not touched |
| F3 | held | `+If nothing in the list suits it, pick nothing and answer with an empty reply`: makes "none" explicit, which the line already allows; the model still chooses how many. |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | not touched: the product list is still built from every in-stock product, with no pre-filter. |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched in code: an empty or chatter-only answer still returns `[]` with no fallback; the new tests only assert this. |
| C5 | held | not touched |
| C6 | held | not touched: still a single `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: no