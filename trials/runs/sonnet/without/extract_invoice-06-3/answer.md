Invoices with single-amount charges like delivery, setup fees and annual fees now load. A Northgate-style invoice comes through with both lines, the delivery at 35.00, `lines_total` 285.00 and status `ok`. All 15 tests pass.

**What changed in `seam.py`**
- **Single-amount lines:** a line with no quantity but a price (`unit_price`) or an `amount` is treated as quantity 1 at that amount. A line with no quantity and no price at all still fails with `line N quantity is missing`.
- **Prompt:** it now tells the model that a charge printed as one amount should come back as quantity 1 with that amount as the unit price. This means the usual answer already has the right shape.

**What changed in `test.py`**
- **Replaced test:** I replaced `test_missing_quantity_is_an_error`, which asserted that a "Delivery" line with only a price is an error. That is the behaviour you reported as the bug.
- **New tests:** the new tests use the Northgate invoice in three shapes the model might return: null quantity with a price, only an `amount`, and everything null except `amount`. They also check that a line with no price at all still errors.

**Trade-off:** a line with a missing quantity and a price is now assumed to be quantity 1, even if the model dropped a real quantity, for example "12 boxes at 24.50". In that case the lines won't sum to the total, so the invoice comes back as `mismatch` and goes to a clerk rather than into the ledger. If that seems too loose, say so and I can restrict the assumption to lines where the model supplies `amount` explicitly.