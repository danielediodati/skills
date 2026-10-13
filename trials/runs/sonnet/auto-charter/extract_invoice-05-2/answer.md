I haven't changed anything, because the fix needs a change to the extractor's charter, and only you can make that.

**Why Brightwell BP-2291 is flagged:** the extractor only knows lines and a total. It reads 309.00 from the lines, 370.80 as the amount due, and compares them for exact equality. The 61.80 of VAT is not a line, so the sum can never match. The charter says this outright: "Invoices whose total includes tax or shipping that is not a line will show as `mismatch` by design" (`evals/extract_invoice/charter.md`, Target and budget).

**Which lines are in the way:**
1. **Status check (constrained, in code):** "exact equality of lines_total and total, with no tolerance". Making VAT invoices pass means the check becomes something like `lines_total + tax == total`, which is a different check.
2. **Output shape (constrained, in the prompt):** the model is asked for exactly six keys, and code depends on those names. Code can't know the VAT amount unless the model reports it, so the prompt would need a seventh key.

I can't work around this inside the charter. For example, telling the model to report the pre-tax subtotal as "total" would make the status come out `ok`, but that dictates the answer the charter leaves to the model's judgement. It would also put a figure that isn't the amount due into the ledger.

**What moving the lines would buy, and cost:**
- **Gain:** invoices whose lines plus stated tax equal the amount due go straight to the ledger, and the review pile holds only real discrepancies such as a wrong quantity or a mistyped total.
- **Cost:** the tax figure would come from the model's reading, so a model that misreads could report a tax that happens to make things balance. The check stays exact, with no tolerance, but it no longer rests only on the lines and the total.
- **Mitigation:** code could also require the tax to be non-negative, or to be consistent with a stated rate if the model reports one. That is a further decision for you.

**What I'd do if you approve:**
- Add an optional `tax` key to the prompt, defaulting to zero when the invoice shows none.
- Change `status` to `ok` when `lines_total + tax == total`, still with exact equality.
- Add tests for the Brightwell case (309.00 + 61.80 = 370.80) and for a VAT invoice with a wrong total, which must still be a mismatch.
- Update the charter and README to match.

Tell me if you want this, and whether the charter's "by design" note should be replaced with the new rule. Shipping charges are not covered by this change. If a supplier shows delivery outside the line items, those invoices will still be flagged.