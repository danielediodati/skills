Invoices whose own figures are consistent now go straight to the ledger, and the Brightwell invoice (BP-2291) comes out `ok`. All 18 tests pass.

**What was wrong:** the tool compared the lines (309.00) against the amount due (370.80), so any invoice with VAT looked like a mismatch.

**What changed in `seam.py`:**
- The model now reads three separate figures from the invoice: `net`, `vat` (0 if the invoice has none) and `total`.
- Code checks, to the cent and with no tolerance, that the computed lines add up to `net` and that `net + vat` equals `total`. Only if both hold is the status `ok`.
- A wrong quantity, a mistyped total or VAT that doesn't match still goes to a clerk.
- The result now also carries `net` and `vat`.
- If the model leaves out `net` or `vat`, the tool raises an `InvoiceError`, as it does for any other missing field.

**Also updated:** `README.md`, and `test.py`. The tests now cover the Brightwell case, an invoice with no VAT, a net that differs from the lines, and a total that differs from net plus VAT.

**Charter:** this is the item the extract_invoice charter already listed as constrained and "not yet in code", so no line moved and I left the charter untouched.

**Reading VAT:** an invoice that states VAT only as a percentage, or has no clear net subtotal, depends on how well the model reads it. If it misreads, the invoice goes to a clerk, which is the safe direction.