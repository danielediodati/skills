Your three failing amounts now load as numbers, and an amount that can be read two ways is still refused. The 18 tests pass.

- **Parsing:** `_number` in `seam.py` handles string amounts in code, so the model's prompt and the single model call are unchanged.
- **Formats read:**
  - `1.234,56` and `1,234.56` both give 1234.56.
  - `£1,234.56` gives 1234.56.
  - `1'050.00 CHF` and `CHF 1’050.00` give 1050.00.
  - `1 234,56 €` gives 1234.56.
  - `-1.234,56` and `12.50-` are read as negative, since discounts and credit notes are real content.
- **Refused as before:** `1,234` and `1.234` (a single separator followed by exactly three digits) are refused with `... is not a number: '1,234' (separators can be read two ways)`. An amount like `0,335` is still read as a decimal, because a leading zero cannot be a thousands group.
- **Also refused:** malformed groupings such as `1,23,456`, `1.234,56,7` and `1,`.
- **Numbers from the model:** JSON numbers (`24.5`) go through exactly as before.

Two behaviour changes to be aware of:
- A string amount like `"1.234"` that used to load as 1.234 is now refused. If the model sometimes sends machine-style strings with three decimals, those invoices will go to a clerk.
- Unit text next to a quantity (`12 pcs`) is now read as 12, because trailing letters are treated like a currency code.

This stays inside the charter's "mechanical steps" constraint, so no decision moved to or from the model. I added one line to `evals/extract_invoice/charter.md` and a sentence to `README.md` recording it, and added tests in `test.py`.