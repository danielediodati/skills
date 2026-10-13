I haven't changed anything, because fixing this means moving a line in the `extract_invoice` charter, and only you can do that.

**Why Brightwell goes to review**

The model correctly reports the amount due as 370.80. The code adds the lines to 309.00 and compares the two with exact equality, so any invoice that charges VAT is a mismatch. The code never sees the 61.80 of VAT, so it cannot tell a VAT difference from a real error.

**The line**

The charter's "Constrained" section says status is `ok` only if `lines_total == total` exactly, with no tolerance. This decision stays in code. Every way I can see to make the Brightwell invoice pass moves that line or another one:

- **Check against the net figure:** asking the model to report the pre-VAT subtotal as `total` would let the existing check pass. But the charter lists "which figure is the total (the amount due)" as the model's free decision, and a prompt that dictates the answer takes it over. The record would also stop holding the amount due, which is the figure the ledger needs.
- **Loosen the check:** a tolerance, or "pass if `lines_total` is within some percentage of `total`", is the loosening the charter rules out. It would also let through real errors that happen to be close.
- **Add the VAT to the check:** the model would additionally read the VAT amount, and the code would require `lines_total + vat == total` exactly, still with no tolerance. This is the option I'd recommend, since it keeps the check strict and the arithmetic in code. The model's reading would be one new field, `vat`, and a missing `vat` would count as zero. A wrong quantity or a mistyped total would still be a mismatch, because the three figures would no longer add up. It is still a change to the Constrained status rule and to the output shape, so it needs your decision.

If you choose the third option, I'd update the charter to match (you make that edit), then change `seam.py`, the prompt and the tests. Before any paid check on real invoices, we'd agree a spending budget. The Brightwell invoice and a mistyped-total case can be covered by free local tests first.

Decision for you: should the status check become `lines_total + vat == total` with the model reading `vat`, or would you prefer a different approach?