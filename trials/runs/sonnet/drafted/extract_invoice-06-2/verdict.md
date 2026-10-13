## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ A charge printed as a single amount, such as delivery, a setup fee or an annual support fee ... report it as one line`: a general rule on how to report such a charge; the model still reads each invoice to decide which entries are such charges. |
| F5 | held | not touched |
| F6 | held | `+ report it as one line with "quantity" 1`: applies only to charges printed without a quantity; code adds no whole-number rule and quantities elsewhere stay free. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | not touched: the `_number(raw.get("quantity"), ...)` check still raises `InvoiceError` on a missing quantity; code adds no default. |
| C2 | held | not touched: the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched: the gap (total is the amount due, no net/VAT fields) is left as it was. |
| C4 | held | `+ "quantity" 1 and "unit_price" equal to that amount`: the model reports a printed figure as unit price; `_cents(quantity * unit_price)` still computes every amount in code. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: no