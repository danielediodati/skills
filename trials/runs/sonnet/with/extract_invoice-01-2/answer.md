Amounts written the way your suppliers write them are now read as the numbers they are, and the full test suite passes (17 tests, including new ones for this).

**The three from last week**
- `1.234,56` and `1,234.56` both read as 1234.56.
- `£1,234.56` reads as 1234.56.
- `1'050.00 CHF` reads as 1050.00.

**What is read**
- **Separators:** thousands separators of `.`, `,`, `'` or a space (including non-breaking), with a decimal comma or point.
- **Currency:** a symbol or code before or after the amount, such as `EUR 1 234,56` or `1 234,56 €`.
- **Sign:** a minus before the amount or after it.

**What is still refused**
- **Ambiguous amounts:** `1,234`, `1.234` and `£1,234` raise `InvoiceError` with `total is ambiguous: ...`, since nothing in them says whether the separator is a thousands mark or a decimal.
- **Unambiguous cases:** `0.335`, `12,5`, `1,234,567` and `1.234,56` are read without guessing.
- **Malformed amounts:** things like `1,23,456`, `1 234'567` or `5 EUR 6` still raise `is not a number`.

**One behaviour change**
A string `"1.234"` from the model was previously loaded as 1.234. It is now refused as ambiguous, which follows your preference. A JSON number from the model, such as `1.234`, is untouched.

**Where it lives**
- **Code:** the change is in `_number` in `seam.py`. The prompt and the model's freedoms are unchanged.
- **Charter and README:** I added the amount reading to the mechanical steps in the charter and a paragraph to the README. No line between model and code moved.
- **Tests:** the new cases are in `test.py`.