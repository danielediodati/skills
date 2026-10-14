Brightwell BP-2291 now passes the check: 309.00 net, 61.80 VAT, 370.80 due comes out `ok` and goes to the ledger. All 19 tests pass, including the new ones.

**What was wrong:** the model was asked for `total` as the amount due, which includes VAT. The check compared the lines' net sum (309.00) with that VAT-inclusive figure, so every invoice that charges VAT failed.

**What I changed in `seam.py`:**
- The extraction now also asks for `subtotal` (before VAT) and `vat` (the VAT amount, 0 if none).
- `status` is `ok` only when the lines equal the subtotal and subtotal + VAT equals the total. Otherwise it is `mismatch`.
- If the model doesn't return a subtotal, the total is used as the subtotal. If it doesn't return VAT, VAT is taken as 0. So a VAT invoice with no breakdown still goes to review rather than passing silently.
- The result dict gains `subtotal` and `vat`.

**Tests (`test.py`):** I added cases for the Brightwell figures passing, a wrong VAT amount being a mismatch, a wrong subtotal being a mismatch, a VAT-inclusive total with no breakdown being a mismatch, and an unreadable VAT value raising an error. `README.md` is updated to match.

**Limits to be aware of:**
- The check is only as good as the model's reading. If the model works VAT out itself instead of copying it from the page, a wrong total could be made to look consistent. The prompt asks for the printed figures, but nothing enforces that.
- I check the arithmetic only, not that the VAT matches the rate on the invoice.
- I haven't run a real invoice through the model; the tests use fake model answers.
- This folder isn't a git repository, so I didn't commit anything.