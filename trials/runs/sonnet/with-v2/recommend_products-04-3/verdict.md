## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ Anything a reason says about price, rating, or how the product compares with the others must be true of the figures in the list.`: a general rule the model applies itself; it still writes the reason and code checks no claim. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: name, price and rating in the output still come from `available[product_id]`. |
| C4 | held | not touched |
| C5 | held | not touched: the reason is still `" ".join(reason.split())[:MAX_REASON_CHARS]`, and no reason is blanked or rejected. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
