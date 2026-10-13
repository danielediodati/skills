## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched: the prompt still asks for `"lines"` with no rule on which entries count as lines. |
| F5 | held | not touched: `+ net = _cents(_number(data.get("net"), "net"))` and the `vat` line put no sign rule on the new amounts. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ net = _cents(_number(data.get("net"), "net"))` and `+ vat = _cents(_number(data.get("vat"), "vat"))`: the new named keys raise `InvoiceError` naming the field when missing or malformed. |
| C2 | held | not touched: the gap is as it was, the code still only checks three capital letters. |
| C3 | moved toward the charter | `+ "net" (the amount before VAT), "vat" (the VAT amount, 0 if the invoice charges none)` and `+ consistent = lines_total == net and net + vat == total`: separate fields, with the arithmetic checked by code. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ consistent = lines_total == net and net + vat == total`: exact equality to the cent, no tolerance, otherwise `mismatch`; the lines reach the total through net and VAT as C3 asks. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry, and a missing `net` or `vat` raises instead of falling back. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
