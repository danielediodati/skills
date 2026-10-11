Amounts written with thousands separators, a decimal comma or point, and a currency symbol or code are now read as numbers. The change is in `_number` in `seam.py` (new helper `_parse_amount`), and all 17 tests pass, including new ones for this.

**Now read correctly**
- `1.234,56` and `1,234.56` both give 1234.56.
- `£1,234.56`, `EUR 1 234,56` and `$ 99` read with the currency stripped.
- `1'050.00 CHF` gives 1050.00.
- Negatives are also read: `-€12,50` and `(12.50)`.

**Still refused, with today's `... is not a number` message**
- A lone separator followed by exactly three digits, such as `1,234` or `1.234`. It can't be told apart as thousands or decimal, so it is not guessed. The message adds `(separator is ambiguous)`.
- Inconsistent grouping such as `1,23.456`, and stray text such as `12 EUR 5`.
- Decimals that clearly can't be thousands are still accepted, for example `0.335`, `12,5` and `1234,567`.

**Behaviour change**
- A plain string like `"24.500"` was accepted before and is now refused as ambiguous. Numbers sent as JSON numbers are unaffected.

This is a code-side parsing step, so it stays within the charter. I did not touch the prompt or the charter, and the model is still called once.