## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ def _strip_affix(text):` drops symbols and codes from amounts only; the `currency` field still comes from the model's answer. |
| F4 | held | not touched |
| F5 | held | `+_SIGNS = {"-": "-", "−": "-", "+": ""}`: signs are read and kept, so negative amounts pass as before. |
| F6 | moved toward code | `+ if len(tail) == 3 and head not in ("", "0") and len(head) <= 3:` / `+ return ""`: `_number` also reads quantities, so a string quantity such as `"1.234"` or `"2.500"` is now refused by rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ raise InvoiceError(f"{label} is not a number: {value!r}")`: an unreadable or ambiguous amount still raises, naming the field; keys, date and line checks not touched. |
| C2 | held | not touched; the gap stays as it was (only three capital letters checked). |
| C3 | held | not touched; the gap stays as it was (total is still the amount due). |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | not touched; `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched; the prompt and the single `model(...)` call are unchanged. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
