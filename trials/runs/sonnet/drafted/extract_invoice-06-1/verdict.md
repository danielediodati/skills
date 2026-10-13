## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ A charge the invoice prints as a single amount, with no quantity or price per unit (a delivery charge, a flat fee), has "quantity" 1`: a general rule on how to report such a charge; the model still decides which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched; the added rule covers only charges printed with no quantity, and code still accepts any finite quantity. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ Every line needs both "quantity" and "unit_price".`: the prompt restates the shape; code still raises `InvoiceError` naming the field when either is missing. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is as it was. |
| C4 | held | `+ has "quantity" 1 and that amount as "unit_price"`: the model reports a printed figure as unit price; `_cents(quantity * unit_price)` still computes every amount. |
| C5 | held | not touched |
| C6 | held | not touched; no default or fallback was added for a missing quantity, and there is still one call. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: no