Amounts like `1.234,56`, `£1,234.56` and `1'050.00 CHF` are now read as the numbers they are, and genuinely ambiguous ones are refused. I could not re-run the suite after my last edit because the shell was blocked. The previous run had 15 of 17 passing, and the 2 failures were wrong expected values in my new test, which I corrected.

**What changed**
- The parsing is in `seam.py`, inside `_number`. It only applies to amounts that arrive as strings; JSON numbers are handled exactly as before.
- Accepted:
  - Thousands separators: `.`, `,`, `'`, `’`, space, no-break space.
  - Decimal comma or decimal point.
  - A currency symbol or 3-letter code before or after the amount (`£`, `€`, `US$`, `EUR`, `CHF`).
  - A minus sign before or after.
- When both `.` and `,` appear, the last one is the decimal separator, and the other must group digits in threes (`1.234.567,89` is fine).
- Refused with the same `... is not a number` message:
  - Inconsistent groupings, such as `1,23,456.78`.
  - Several signs, such as `--5`.
  - Stray text, such as `three hundred`.

**Ambiguous amounts**
- A single separator followed by exactly three digits is refused, for example `1.234`, `1,234`, `£1,234` or `12.345 CHF`. It could be a thousands group or three decimals, and nothing in the text settles it.
- The message then ends with "(it could be read two ways)".
- `0.335` and `1234.567` are still read as decimals, because a leading `0` or more than three leading digits rules out a thousands group.

**Behaviour change**
A string `"1.234"` used to load as 1.234 and is now refused. If the model returns the printed text, it is a real guess. If you would rather keep the old reading for plain-point strings, it is a one-line change.

**Tests**
- New tests in `test.py` cover the formats above, the ambiguous cases and the inconsistent separators.
- Run them with `python -m unittest`.

Currency markers such as `kr` or `Fr.` are not recognised, so those amounts are still refused.