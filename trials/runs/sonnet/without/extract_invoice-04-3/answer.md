Invoices with continental amounts now load with the right figures: "1.250,00 EUR" gives a total of 1250.00, and "2.340,50" gives a unit price of 2340.50. The tests pass, including new ones for these cases.

**What changed**
- **Amount parsing:** `_number` in `seam.py` now reads amounts the way they are printed. This covers:
  - `1.250,00` and `1,250.00`
  - `1 250,00`, with a normal or non-breaking space
  - `1'250.00`
  - `1.234.567`
  - a leading `€` or trailing `EUR`
  - a minus sign
- **Prompt:** it now asks the model to write amounts as plain numbers with a decimal point. Parsing no longer depends on the model following this, but it should mean fewer odd formats arrive.
- **Tests:** `test.py` has new cases for the formats above, the ambiguous case below, and malformed groupings.

**One behaviour change you should know about**
A lone separator followed by exactly three digits, such as `1.250` or `1,250`, is now refused with `total is ambiguous, thousands or decimals: '1.250'`. It could mean 1250 or 1.25, and guessing wrong would load an amount that is a thousand times too small. Values like `0.335` and `15.00` are unaffected. The same applies to a quantity such as `2.500` kg, which will now go to a clerk instead of loading.

Malformed groupings such as `1.25.0,00` are still rejected as "not a number".

If you would rather resolve the ambiguous case automatically, for example by treating it as thousands when the supplier is German, that needs the supplier's country passed in. I haven't added that.