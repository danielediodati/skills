Invoices with single-amount lines now load. The Northgate invoice (NF-0718) comes through with two lines, Delivery at 35.00, and a total of 285.00 that matches. All 18 tests pass.

**What was wrong:** `extract_invoice` in `seam.py` required a `quantity` on every line and raised `line N quantity is missing` when it was absent. A delivery, fee or setup charge has no quantity, so it was rejected.

**What I changed:**
- **`seam.py`**: a line with no quantity (null, absent or blank) is now treated as one unit, so its amount is its `unit_price`. I also added a sentence to the model prompt telling it to report single charges as `"quantity": 1` with the amount in `unit_price`.
- **`test.py`**: I replaced the old test that asserted "missing quantity is an error". The new tests cover:
  - the Northgate invoice loading with status `ok`
  - a delivery line and an annual-fee line with the quantity missing or left out
  - a line with no `unit_price` still raising an error
  - a missing quantity on a line that doesn't reconcile still producing `mismatch`
- **`README.md`**: documents the single-charge rule.

**Choices you may want to revisit:**
- A missing quantity is read as 1 even on a line that is really multi-unit. The total check is the safeguard: if the lines don't add up to the total, the invoice is still marked `mismatch` and goes to a clerk. I did not add a separate check for that case.
- A line with a quantity but no `unit_price` still fails. I didn't widen the rule to cover it because none of your examples needed it.

I only tested against the fake model in the test file, so I haven't confirmed how the real model answers a delivery line. The prompt change is there to steer it toward `quantity: 1`, but if a real invoice still fails, run it through the live model and check its JSON.