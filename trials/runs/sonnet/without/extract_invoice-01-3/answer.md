The three invoices from last week's log now load: `1.234,56`, `£1,234.56` and `1'050.00 CHF` are read as 1234.56, 1234.56 and 1050.00. The full test suite passes, including new tests for these cases.

**What changed** (in `_number` in `seam.py`):
- **Thousands separators:** `.`, `,`, `'` (also `’`), and ordinary or non-breaking spaces are accepted. Grouping must be valid, so `12 34` or `1,23.456,7` are refused.
- **Decimal marks:** when both `.` and `,` appear, the last one is the decimal mark. A single separator not followed by exactly three digits is the decimal mark, so `12,50` is 12.50.
- **Currency:** symbols and letter codes are stripped from either end, and a sign may sit on either side of them (`-£5`, `£-5`).
- **Ambiguous amounts are refused:** `1.234`, `1,234`, `£1,234` and `999.999 EUR` fail with `total is ambiguous, '.' may be a decimal or a thousands separator: '1.234'`. This is a different message from `is not a number`, so you can tell the two kinds of refusal apart in the log.
- **Unchanged:** a leading `0` (`0.335`) and more than three digits before the separator (`1234.567`) can only be decimals, so they still parse as before.

**One behaviour change to be aware of:** a string amount such as `"1.234"` used to be read as 1.234 and is now refused. Real JSON numbers (`1.234`) are untouched. If your model usually returns unit prices to three decimals as strings, you will see more refusals of that kind, and they will say "ambiguous" in the message.

I also added a short paragraph on this to `README.md`.