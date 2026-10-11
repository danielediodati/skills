Invoices written with European number formatting now load with the right figures. The Kessler total `"1.250,00"` comes through as `1250.00`, and the Cartiera Lombarda `"2.340,50"` unit price as `2340.50`. All 17 tests pass, including the new ones.

**What changed** (in `seam.py`, in `_number`)

- **Both separators present:** the last one is the decimal mark. `1.250,00` and `1,250.00` both give `1250.00`.
- **One kind repeated:** these are thousands marks, so `1.250.000` gives `1250000`.
- **A single separator with a number of digits other than three after it:** this is a decimal mark, so `15,5` gives `15.5`.
- **Spaces, non-breaking spaces and apostrophes:** these count as grouping, so `1 250,00` and `1'250.00` both work.
- **Plain JSON numbers:** these are untouched.

**One deliberate limit:** a lone separator followed by exactly three digits, such as `1.250` or `1,250`, is refused with `total is not a number: '1.250' (ambiguous separator)`. That could be 1250 or 1.25 depending on the country, and guessing wrong would put a figure 1,000 times too large or too small into the ledger. The exception is a leading zero, so `0.335` is still read as a decimal.

This means a value like `1.250` that used to load as 1.25 is now refused. The ambiguity only arises when an amount is printed without cents, and those invoices go to a clerk with a clear reason. If you'd rather resolve it automatically, for example by treating it as a thousands mark whenever the supplier is German, that needs the supplier's country passed in. Say if you want that.

I added tests for the formats above, for the Kessler total, and for the ambiguous and malformed cases.