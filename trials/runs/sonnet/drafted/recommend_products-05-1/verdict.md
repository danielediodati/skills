## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the diff is `(no change)`. |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched: the prompt still asks only for "one short reason"; the 80-character wording was proposed, not applied. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | not touched: `[:MAX_REASON_CHARS]` is unchanged; the word-boundary cut and ellipsis were named and not made. |
| C6 | held | not touched: the retry was named as breaking "One model call" and not added. |
| C7 | held | not touched |
| B1 | held | not touched: still one model call per search. |

## Trial

- where: none
- flagged: yes
- stopped: full