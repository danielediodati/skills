VAT invoices now come back `ok` when the lines plus the tax equal the total. The 17 tests pass, including three new ones; your stationery example is covered by `test_tax_is_reported_and_added_to_the_lines`.

- **Tax reported:** the model is now asked for a `tax` amount, and the result carries `tax` next to `lines_total` and `total`.
- **Status check:** status is `ok` when `lines_total + tax == total` to the cent, with no tolerance, and `mismatch` otherwise. Code does the arithmetic.
- **No-tax invoices:** if the model gives no tax, `tax` is `0.00` and the check is the same as before.
- **Prompt change:** the prompt now says lines are net of tax and the total includes tax.
- **Files touched:** the changes are in `seam.py`, `test.py` and `README.md`. This matches the charter's "Net, VAT and total as separate fields" item, so I did not edit the charter.

If the model misses the tax on a VAT invoice, the result is `mismatch`, so it goes to a clerk rather than into the ledger.