## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `re.sub(r"(?<![A-Za-z])[A-Za-z]{3}(?![A-Za-z])\|[€$£]", "", value)` strips a currency mark from amount strings only; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `sign, text = text[0] if text[0] == "-" else "", text[1:]` keeps the minus sign; negative amounts pass as before. |
| F6 | moved toward code | `+ if len(fraction) == 3 and whole != "0": raise InvoiceError(f"{label} is ambiguous, thousands or decimals: {value!r}")` also runs on `quantity`. A quantity answered as `"1.250"` (1.25 kg), read as 1.25 before, is now refused by a code rule. |
| C1 | held | `+ text = _plain_number(value, label)` reads more written forms of a number, but an unreadable amount still raises `InvoiceError` naming the field (`raise bad()`). Keys, date format and the at-least-one-line check are not touched. |
| C2 | held | not touched; the gap stays as it was (`[A-Z]{3}` check unchanged). |
| C3 | held | not touched; the gap stays as it was. |
| C4 | held | `+Write amounts as plain numbers with a "." decimal point and no thousands separator` asks for a notation, not arithmetic. `amount` is still `_cents(quantity * unit_price)`. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
