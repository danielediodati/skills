Amounts written the way your suppliers write them are now read as the numbers they are, and the three examples from last week's log load correctly. The suite, with the new tests, passes (17 tests).

**What changed**
- The reading logic is in `seam.py` (`_number` and a new `_written_amount`).
- `README.md` documents the new behaviour.
- `test.py` has new tests for the accepted, ambiguous and malformed cases.

**What is read now**
- **Examples:** `1.234,56`, `1,234.56`, `£1,234.56`, `1'050.00 CHF`, `EUR 1 234,56`, `-£1,234.56` and `1,234,567` all work.
- **Separators:** `.`, `,`, `'`, `’`, a space and non-breaking or thin spaces count as thousands separators.
- **Decimals:** when a comma and a point both appear, the last one is the decimal separator. A single separator with anything other than three digits after it is a decimal (`12,5`, `0.335`, `1234.567`).
- **Currency:** a symbol or code before or after the amount is ignored (`£`, `€`, `CHF`, `Fr.`, `US$`).

**What is refused**
- **Ambiguous amounts:** `1.234` and `1,234` could be one thousand two hundred thirty-four or one and 234 thousandths, so they are refused with `total is ambiguous: '1.234'`.
- **Malformed amounts:** mismatched or misplaced groupings (`1,23,456`, `1.2.3`, `12 34`, `1,234.567,89`), a trailing separator, and stray words are refused with `is not a number`.

**Things to be aware of**
- A string like `"1.234"` used to load as 1.234. It is now refused, because that exact form is how an Italian `1.234` (one thousand two hundred thirty-four) would arrive. Numbers the model sends as real JSON numbers are untouched.
- Three-decimal quantities such as `1.250` kg, sent as a string, will also be refused, since they are ambiguous in the same way.
- Indian lakh grouping (`1,23,456`) and negatives written `(123.45)` or `123.45-` are refused rather than guessed. Say if you want them supported.
- The currency printed on an amount is not compared with the invoice's `currency` field.