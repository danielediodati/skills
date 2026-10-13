I haven't changed anything, because this fix can't be made without moving a line the charter fixes. The decision is yours.

**Why Brightwell is marked a mismatch.** In `seam.py:71`, `status` is `ok` only when `lines_total == total` exactly. For BP-2291 that compares 309.00 (net lines) with 370.80 (amount due), so every invoice that charges VAT is flagged. The tool has no concept of tax.

**The line.** The charter (`evals/extract_invoice/charter.md`) makes three things constrained:
- The comparison is "lines_total equals total exactly (zero tolerance)", fixed in code.
- The output keys and types are fixed, because the ledger loader depends on them.
- The prompt fixes the requested keys.

Any way of making Brightwell pass changes at least one of these: a new tax term in the comparison, a tax key in the prompt, or a new field in the output. I can't do the useful part of this without crossing the line, so I'm stopping here.

**What I'd propose, if you approve moving it:**
1. The prompt also asks the model to read the tax amount printed on the invoice, as `tax`. Reading it is a judgement the model is already making for the total.
2. Code compares `lines_total + tax == total`, still exactly and still in `Decimal`. An invoice with no tax figure is treated as tax 0.00 only when the model returns it explicitly. A missing key raises `InvoiceError`, as the other required fields do.
3. The output gains `tax`, and `lines_total` keeps its meaning. Whether the ledger loader tolerates a new key is for you to confirm.
4. I'd add tests for Brightwell (309.00 + 61.80 = 370.80 gives `ok`), a mistyped total with VAT (still `mismatch`), and a no-VAT invoice.

**What it buys, and the risk.** Correct VAT invoices go straight to the ledger, and the review pile holds only invoices whose figures really disagree. The cost is that the check now trusts a second model-read figure. A model that misreads the tax could make a wrong total look consistent, or flag a correct invoice. A cheap guard is to keep `tax` visible in the output so a clerk can see it.

**Decisions for you:**
- Do you approve moving the comparison, the prompt and the output shape as described?
- Should the charter be updated to match? Only you can edit it, so I'd leave that to you.
- If you approve, any eval or model run beyond the free local unit tests needs your approval and a spending budget first.