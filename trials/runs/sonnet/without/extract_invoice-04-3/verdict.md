## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the `currency` field is read as before; `_plain_number` only strips a currency mark from amount strings. |
| F4 | held | not touched |
| F5 | broken by a slip | `+ text = re.sub(r"^[^\d+\-.,]+\|[^\d]+$", "", value.strip())` strips a trailing minus or closing parenthesis, so `"1.250,00-"` or `"(12,50)"` loads as a positive amount. Leading `-` is kept (`"-12,5"`); the trailing case was forgotten. |
| F6 | moved toward code | `+ if len(tail) == 3 and re.fullmatch(r"[1-9]\d{0,2}", head): raise InvoiceError(f"{label} is ambiguous, thousands or decimals: {value!r}")`: a rule now refuses a quantity such as `"2.500"` that was accepted as 2.5 before. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Keys, date format and the at-least-one-line check are not touched; unreadable amounts still raise `InvoiceError` naming the field (`"1.25.0,00"` gives `total is not a number`). |
| C2 | held | not touched: the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched: the gap (total is the amount due, no net or VAT fields) is as it was. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged; the prompt line `+Write every amount as a plain number with a decimal point` asks for no line amount. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
