## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+_CURRENCY = rf"(?:[A-Za-z]{{3}}\|[A-Za-z]{{0,2}}[{_SYMBOLS}]+)"` only strips a marker next to an amount; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `+    return -number if signs == ["-"] else number`: negative amounts are still accepted, now also with a trailing minus or a currency marker. |
| F6 | moved toward code | `+        raise _Ambiguous  # 1.234 or 1,234: thousands or three decimals` sits in `_number`, which also reads `quantity`: a string quantity such as `"2.500"` loaded before and is now refused by a code rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+            raise InvoiceError(f"{label} is not a number: {value!r} (it could be read two ways)")`: keys, date format and the at-least-one-line rule are untouched, and an unreadable amount still raises naming the field. |
| C2 | held | not touched: the `currency` field is still checked only as three capital letters, so the gap is as it was. |
| C3 | held | not touched: the total is still the amount due, so the gap is as it was. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
