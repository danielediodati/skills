Invoices with a single-amount line such as a delivery, setup or support fee now load. A line with no quantity is read as one unit, so the Northgate invoice comes through as two lines, with delivery at 35.00 and a total of 285.00 that matches. All 16 unit tests pass.

Changes, all in this folder:

- **`seam.py`**: a line with no `quantity` now defaults to 1. A line with no `unit_price` still raises an error. I also added one sentence to the model prompt telling it to report a lump-sum charge as quantity 1 with its amount as the unit price.
- **`test.py`**: I replaced `test_missing_quantity_is_an_error`, since it encoded the behaviour you want changed. The new tests cover:
  - the Northgate case (40 brackets plus a delivery line, total 285.00, status `ok`);
  - a missing quantity on a genuinely multi-unit line, which comes back as `mismatch`;
  - a missing unit price, which still raises an error.
- **`README.md`**: I documented the one exception to "missing fields raise an error".

A line read as one unit that was really multi-unit won't be loaded silently. The lines won't add up to the total, so the invoice goes to a clerk as `mismatch`, as it does today.

I haven't run this against the real Northgate PDF or the other invoices, only the unit tests with the same figures. The model still has to return the delivery line in a form the code accepts. The prompt change should make that likely, but a real run is the test that settles it.