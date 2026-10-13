## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ no currency symbols` applies only to the quantity, unit price and total values; the model still infers the `currency` field. |
| F4 | held | not touched |
| F5 | held | `+ Write every quantity, unit price and the total as a plain decimal number` fixes notation only; sign is not restricted and code still accepts negatives. |
| F6 | held | `+ digits with a dot as the decimal separator` keeps fractional quantities; no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | not touched: `_load_json`, `_text`, `_number` and the date and lines checks are unchanged, and malformed numbers still raise `InvoiceError` naming the field. |
| C2 | held | not touched: the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched: the gap (no separate net, VAT and total) is left as it was. |
| C4 | held | not touched: `_cents(quantity * unit_price)` is unchanged; the prompt asks the model to transcribe figures, not to compute amounts. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance. |
| C6 | held | not touched: still a single `model(PROMPT.format(text=text))` call, with no retry or fallback. |
| C7 | held | not touched: the empty-text refusal, JSON extraction and `.upper()` are unchanged. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
