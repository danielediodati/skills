## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `[A-Za-z]{3}` and `[€$£]` are stripped from amount strings only; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `+ sign, text = text[0] if text[0] == "-" else "", text[1:]`: the minus sign is kept through the new parser, so negative amounts still pass. |
| F6 | moved toward code | `+ if len(fraction) == 3 and whole != "0": raise InvoiceError(f"{label} is ambiguous, thousands or decimals: {value!r}")`: a rule added on purpose that refuses a quantity such as `"1.250"` (kilos, metres), read as 1.25 before. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ text = _plain_number(value, label)`: amounts are still checked by code, and every refusal still raises `InvoiceError` naming the field (`{label} is not a number`, `{label} is ambiguous`). |
| C2 | held | not touched: the gap is as it was, currency is still only checked as three capital letters. |
| C3 | held | not touched: the gap is as it was, the total is still the amount due. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged, and the prompt still does not ask the model for line amounts. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry or fallback added. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
