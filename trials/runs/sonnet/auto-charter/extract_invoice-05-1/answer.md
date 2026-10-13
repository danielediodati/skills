I haven't changed anything. The fix means moving a line the charter holds in code, and that decision is yours.

**Why Brightwell goes to a clerk**

`evals/extract_invoice/charter.md` fixes the status check as exact equality of `lines_total` and `total`, with no tolerance, and the check is done by code. The model reports the amount due (370.80), the lines sum to 309.00, and the check says `mismatch`. The charter anticipates this and calls it "by design": invoices whose total includes tax that is not a line show as `mismatch`.

**The line in question**

Two constraints would have to change for correct VAT invoices to reach the ledger:

- **The status rule.** It would become `lines_total + tax == total`, or the model would report a subtotal and the code would compare against that.
- **The fixed output shape.** The prompt asks for exactly six keys, and code depends on them. The model would also have to report the tax amount (or the pre-tax subtotal), which is a seventh key.

**What moving it would buy**

- Invoices like BP-2291 (309.00 + 61.80 = 370.80) would pass straight to the ledger, and the review pile would hold only invoices whose figures don't reconcile.
- Zero tolerance can stay: `lines_total + tax == total` is still an exact check in code, not a model verdict.

**What it would cost**

- The model would be trusted for one more figure, the tax. A model that misread the tax could make a wrong invoice look consistent, because the check would no longer compare two independent readings. For example, it could report tax as `total − lines`.
- A cheap partial guard would be a code check that tax is non-negative and not larger than the lines. Alternatively, the model could report the VAT rate and code could verify `tax == lines_total × rate`, which keeps a real cross-check.

**My recommendation**

Add a `tax` key to the model's answer and check `lines_total + tax == total` exactly. Optionally, also require tax to match the stated rate applied to the lines. Invoices without tax would still need `tax` to be 0 or absent, which is a second thing to decide.

If you want this, say so and update the charter yourself, since I can't edit it. After that I'll make the code and test changes.