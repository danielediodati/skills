## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ no thousands separators and no currency symbols` applies to the numeric fields only; the model still infers the `currency` key by reading. |
| F4 | held | not touched |
| F5 | held | `+ Write every quantity, unit_price and total as a plain decimal number` fixes notation only; a sign is still allowed and no code rejects negatives. |
| F6 | held | `+ plain decimal number with a point as the decimal separator` keeps fractional quantities; no whole-number rule added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ Write every quantity, unit_price and total as a plain decimal number` only tells the model how to write; `_number` and every shape check still raise `InvoiceError` unchanged. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net/VAT fields) is left as it was. |
| C4 | held | `+ Write every quantity, unit_price and total` asks for the same inputs as before; the amount is still `_cents(quantity * unit_price)` in code. |
| C5 | held | not touched; `lines_total == total` is still compared to the cent with no tolerance. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry and no fallback parser for a non-plain figure. |
| C7 | held | not touched; the empty-text refusal, JSON extraction and currency upper-casing are unchanged, and no new mechanical step was added in code. |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
