## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ If the reason mentions a price, a rating, or how the product compares with the others, it must agree exactly with the figures in the list below.`: a general rule from the user's requirement that the model applies by reading each list; code still checks no claim. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the returned name, price and rating still come from `available[product_id]`; the added prompt text only asks the reason to agree with them. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
