## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched: the prompt only adds `"subtotal"` and `"vat"` keys, and the model still decides which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | New keys are optional, and `_optional_cents` raises `InvoiceError` naming the field when a figure is malformed. The required keys and the date check are unchanged. |
| C2 | held | not touched: the currency check is still only `[A-Z]{3}`, so the gap stays as it was. |
| C3 | moved toward the charter | `+ subtotal = _optional_cents(data, "subtotal")`, `+ vat = ...`, `+ lines_total + (vat or Decimal("0")) == total`: net, VAT and total are now separate fields, with the arithmetic checked by code. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | The comparison stays exact to the cent with no tolerance, and a failing sum still gives `mismatch`. VAT is now part of the sum under C3. |
| C6 | held | not touched: still one `model(...)` call, no retry and no fallback. |
| C7 | held | not touched |
| B1 | held | not touched: the change adds no model call. |

## Trial

- where: both
- flagged: no
- stopped: no