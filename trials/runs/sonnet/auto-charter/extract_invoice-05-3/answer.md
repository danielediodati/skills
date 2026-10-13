I haven't changed anything. Fixing this means moving a line the charter (`evals/extract_invoice/charter.md`) puts in code, and only you can decide that.

**Why Brightwell goes to a clerk.** The status check compares the sum of the lines (309.00) with the amount due (370.80) using exact equality, so any invoice with VAT that isn't itself a line fails it. The charter says so explicitly: "Invoices whose total includes tax or shipping that is not a line will show as `mismatch` by design." It also lists the zero-cent tolerance as "a deliberate constraint, not a tunable budget."

**The line.** The status is decided by code from `lines_total == total`, because the model's reading must not vouch for itself. Any fix has to let the check accept `lines_total + VAT == total`, which means one of these:

1. **The model reports the tax and code checks `lines_total + tax == total`.** This is the option I'd recommend.
   - It changes the "six keys" output shape and the exact-equality rule.
   - A model that misreads can still choose a tax figure that makes things balance. To contain that, code could also require `tax == rate × lines_total` to the cent, with the rate read from the invoice. That keeps the check mechanical and still catches wrong quantities and mistyped totals.
   - It makes your normal case pass, while a wrong quantity or mistyped total still lands in the review pile.
2. **The model reports the net or subtotal figure, and code compares that with the lines.** This is weaker. Code would then be checking the model's chosen subtotal rather than the amount due, so a mistyped amount due would never be caught.
3. **Accept any total that differs from the lines by up to a percentage.** I'd advise against it. It would let real errors through that are small compared with a 20% VAT.

I'd go with option 1, with the tax-equals-rate-times-net check. If you approve it, I'll update the charter lines you name, then `seam.py`, the prompt, the tests (including Brightwell 309.00 + 61.80 = 370.80 as `ok`, and a mistyped total as `mismatch`), and the README.