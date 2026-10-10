Amounts written with thousands separators, a decimal comma or point, and a currency symbol or code are now read as numbers. The change is in `_number` in `seam.py`, in plain code; the prompt and the charter are untouched. All 17 tests pass, including new ones for these cases.

**Now accepted**
- `1.234,56` and `1,234.56` both read as 1234.56.
- `£1,234.56` reads as 1234.56.
- `1'050.00 CHF` reads as 1050.00.
- A currency symbol or code on either side, a space or apostrophe as thousands separator (`EUR 1 234,56`), and a leading or trailing minus or parentheses for negatives.

**Still refused, with the same error as today**
- Amounts that can be read two ways, such as `1,234` or `€1.234` (a thousand two hundred thirty-four, or one and a bit?).
- Malformed groupings (`1,23,456`, `1,5.00`), stray text inside the number, and two signs.

**Behaviour to be aware of**
- A bare `1.234`, with no currency or sign, is still read as 1.234. That is what the code did before, so I kept it.
- The same text with a symbol (`€1.234`) is refused.
- If a model returns bare strings like that for prices, you could see an inconsistency.

I also added a line about this to the README.