## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ If the search states a price limit or range (...), only pick products whose price is within it.`: a general rule the user stated; the model still reads each search and the prices to apply it. |
| F2 | held | not touched |
| F3 | held | not touched: the added prompt rule fixes no count, and the model may still answer with none. |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | not touched: the `products` list is still built from every in-stock product, with no filter before the call. |
| C2 | held | not touched |
| C3 | held | not touched: the model reads the prices shown, and the returned price still comes from `product["price"]`. |
| C4 | held | not touched: no fallback list added. |
| C5 | held | not touched |
| C6 | held | not touched: still one `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
