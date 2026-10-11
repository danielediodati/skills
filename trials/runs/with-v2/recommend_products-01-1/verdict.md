## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ If the search states a price limit or range (...), pick only products whose price is within it,`: a general rule stated by the user; the model still reads the search and the prices itself. |
| F2 | held | not touched |
| F3 | held | `+ and pick none if no product is.`: part of the same general rule; the model still decides how many, from none to `limit`. |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | not touched; the product list sent to the model is unchanged, with no pre-filter on price. |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched; no fallback list added. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched; still one model call. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
