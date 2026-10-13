I changed the prompt so the model writes European-style amounts as plain decimals, but I haven't tested it against a real model, so I don't yet know that Kessler now loads as 1250.00.

**Cause:** the prompt never said how to write numbers, so the model copied "1.250,00" as printed. The code's decimal check rightly refused it.

**Change in `seam.py`:** the prompt now says that invoices use different national styles (`1.250,00`, `1 250,00`, `1,250.00`). It asks for every quantity, unit_price and total as plain digits with a point for the decimals, no thousands separators and no currency symbol. The model still decides how to read each figure on the page.

**Left alone:** the charter has the code own the number check, so I did not make the code parse European formats. Guessing there would turn an ambiguous "1.250" into silent data. An unreadable figure is still an `InvoiceError`, and `status` is unchanged.

**Tests in `test.py`:**
- The prompt carries the plain-decimal instruction.
- A total of `"1.250,00"` in the model's answer is still rejected with `total is not a number`.
- All 16 tests pass.

**Not verified:** the tests use a fake model, so they only show the prompt carries the instruction. Checking that a real model now returns `1250.00` for the Kessler and Cartiera Lombarda invoices needs a paid run, and none has been made. If you want one, agree a budget with me first. A small set would be enough: the two failing invoices, one UK invoice as a control, and one with a "1.250" style figure that could be read two ways.