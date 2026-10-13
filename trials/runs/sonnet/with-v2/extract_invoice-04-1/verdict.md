## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ ... no thousands separator or currency sign` only governs how amounts are written; the model still infers the currency for the `currency` key. |
| F4 | held | not touched |
| F5 | held | `+ Write every quantity, unit_price and total as a plain decimal number` does not exclude a sign; negative amounts still pass `_number`. |
| F6 | held | `+ digits with "." as the decimal point` keeps non-integer quantities; no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ Write every quantity, unit_price and total as a plain decimal number` is a format rule the model applies by reading; `_number` and the `InvoiceError` checks are unchanged. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | not touched; `_cents(quantity * unit_price)` still computes each amount and the prompt asks for no line amount. |
| C5 | held | not touched; `lines_total == total` is still compared to the cent with no tolerance. |
| C6 | held | not touched; still one `model(...)` call, and no retry or fallback parse is added for amounts the model fails to normalise. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
