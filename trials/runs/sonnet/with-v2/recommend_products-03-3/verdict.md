## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ If a reason mentions a price, it must be exactly the price listed for that same product.`: a general rule the user stated, which the model applies by reading each product; no code checks the claim. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the returned `name`, `price` and `rating` still come from `available[product_id]`; the added prompt line only concerns the free reason text. |
| C4 | held | not touched |
| C5 | held | not touched: the reason is still `" ".join(reason.split())[:MAX_REASON_CHARS]`, and no code blanks it. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
