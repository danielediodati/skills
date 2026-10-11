## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the `currency` field is read as before; `_CURRENCY` only strips a symbol or code next to an amount. |
| F4 | held | not touched |
| F5 | held | `+ rf"(?P<sign1>[-+])?\s*(?:{_CURRENCY}\s*)?(?P<sign2>[-+])?\s*"`: signed amounts are still read (`-£1,234.56`); `(123.45)` and `123.45-` were refused before too. |
| F6 | moved toward code | `+ if len(frac) == 3 and whole[0] not in ("", "0") and len(whole[0]) <= 3:` `+ raise _Ambiguous`: `_number` also reads quantities, so a string quantity like `"1.250"` that loaded before is now refused by a rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ raise InvoiceError(f"{label} is ambiguous: {value!r}") from None`: keys, date and lines check untouched; amounts are still parsed by code and refusals still name the field. |
| C2 | held | not touched: the gap is left as it was, currency is still only checked as three capital letters. |
| C3 | held | not touched: the gap is left as it was, `total` is still the amount due. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged; only how the two operands are parsed changed. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
