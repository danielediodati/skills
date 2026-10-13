## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ no thousands separators and no currency symbol` only governs how amounts are written; the `currency` key and its inference are not touched. |
| F4 | held | not touched |
| F5 | held | `+ decimal number: digits only, a point for the decimals` does not name the minus sign, but it is a notation rule; the model can still report a negative amount and `_number` still accepts it. |
| F6 | held | `+ Write every quantity, unit_price and total as a plain decimal number`: decimals remain allowed for quantities, no whole-number rule added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Shape checks unchanged; `_number` still raises on `"1.250,00"`, as the added test `test_continental_notation_left_in_the_answer_is_still_an_error` confirms. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; total is still the amount due, the gap is left as it was. |
| C4 | held | not touched; `_cents(quantity * unit_price)` still computes the amounts, and the prompt still asks for no line amount. |
| C5 | held | not touched; `lines_total == total` still compares to the cent with no tolerance. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))`, no retry or fallback added. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no