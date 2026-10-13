## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ ... no thousands separator or currency symbol` applies to how numbers are written; the model still infers the `currency` field. |
| F4 | held | not touched |
| F5 | held | `+ Write every number as plain digits with a dot as the decimal separator`: fixes notation only, with no rule on sign; negatives still pass `_number`. |
| F6 | held | `+ ... with a dot as the decimal separator`: decimals stay allowed, and no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `seam.py` code is unchanged; a malformed number still raises, pinned by `+ with self.assertRaisesRegex(InvoiceError, "total is not a number")`. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | not touched; `amount` is still `_cents(quantity * unit_price)` and the prompt asks for no amounts. |
| C5 | held | not touched; `lines_total == total` still decides `status`, with no tolerance. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, and code adds no fallback parse of `"1.250,00"`. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
