## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ If you cannot give a reason for a product, leave that product out.`: a criterion the model applies by reading each product; it still chooses which ones suit. |
| F2 | held | not touched |
| F3 | held | `+ If you cannot give a reason for a product, leave that product out.`: the model still settles the count, from none to `limit`; code imposes no number. |
| F4 | held | `+ say what makes the product worth the customer's attention for it, including when it is not an exact match`: informs the reason without fixing its wording; no code check on its content. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | Code not touched: the reason is still cut by `[:MAX_REASON_CHARS]` and an empty one is still kept. `+ Every line must carry its reason` only asks the model; no pick is dropped or filled. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial