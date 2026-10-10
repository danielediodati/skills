Amounts written the way your suppliers write them are now read as numbers, and the three invoices from your log would go through. All 17 tests pass, including the new ones. I did not re-import last week's invoices.

The change is in `seam.py`: a new `_parse_amount` that `_number` calls for string amounts. Plain JSON numbers behave as before.

**What is read now**
- **Separators:**
  - `1.234,56` and `1,234.56` both give 1234.56.
  - A space, `'` or `’` groups thousands: `1'050.00` gives 1050.00.
  - A repeated mark is grouping: `1.234.567` gives 1234567.
- **Currency:** a symbol (£ € $ ¥ and a few more) or an uppercase three-letter code is accepted before or after the number: `£1,234.56`, `1'050.00 CHF`.
- **Negatives:** `-12,50`, `12,50-` and `(1,234.56)` are all read as negative.

**What is still refused**
- **Ambiguous amounts:** a single separator followed by exactly three digits, like `1.234` or `1,234`, can't be told apart from a decimal, so it is refused with `... is not a number: '1.234' (can be read as 1234 or as 1.234)`.
- **Malformed amounts:** things like `1,23,4`, `1.234,56,7` or `12abc` are refused as well.
- **Edge case:** `0.125` and `1234.567` are accepted, because the leading zero or more than three leading digits settles it.

**Behaviour change**
A string like `"1.234"` used to load as 1.234 and is now refused. That fits your "refuse rather than guess" rule, but it will send more kilos-and-metres quantities such as `2.500` to a clerk. If the model returns those as JSON numbers (`2.5`) they are unaffected.

**Not in scope**
The currency symbol on an amount is dropped and not compared with the invoice's `currency` field.

I didn't touch the charter or the prompt: the model's decisions stay as they were, and this is only the mechanical number reading in code.