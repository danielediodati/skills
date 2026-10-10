## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `body = re.sub(rf"^{_CURRENCY_MARK}\s*\|\s*{_CURRENCY_MARK}$", "", body)` drops the mark on an amount and leaves the `currency` field to the model. |
| F4 | held | not touched |
| F5 | held | `+ negative = negative or body[0] in _SIGNS` and `+ body, negative = body[1:-1].strip(), True`: negative amounts still pass, in more written forms than before. |
| F6 | moved toward code | `+ if len(fraction) == 3 and not grouped and whole != "0" and len(whole) <= 3: raise ValueError(` also runs on quantities: a string quantity like `"2.500"` loaded before and is now refused by a code rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ except ValueError as error: raise InvoiceError(f"{label} is not a number: {value!r} ({error})")`: an unreadable amount still raises `InvoiceError` naming the field; keys, date format and the line minimum are unchanged. |
| C2 | held | not touched: the gap is as it was, currency is still checked only as three capital letters. |
| C3 | held | not touched: the gap is as it was, there are still no separate net and VAT fields. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged; only the reading of the operands changed. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance added. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call; the new parsing is code, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: yes
- stopped: no
