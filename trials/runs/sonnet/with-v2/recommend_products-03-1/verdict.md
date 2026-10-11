## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+If a reason mentions a price, it must be exactly the price listed for that product.`: a general rule the user stated, which the model still applies when writing each reason; no code checks the claim. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: name, price and rating in the output still come from `product[...]`; the added prompt line does not change where they come from. |
| C4 | held | not touched |
| C5 | held | not touched: the reason is still `" ".join(reason.split())[:MAX_REASON_CHARS]`, with no blanking added. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
