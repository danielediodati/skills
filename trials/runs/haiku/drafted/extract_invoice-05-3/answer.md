I haven't changed any code, because the fix you're asking for moves a line that the charter reserves for you.

**Why Brightwell is flagged:** the tool checks `status` by comparing the line amounts (294.00 + 15.00 = 309.00) with `total` (370.80). It never sees the VAT line, so it treats the 61.80 difference as an error. I confirmed this with the existing tests (14 pass) and a dry run using the Brightwell figures, with no model call. The result is `lines_total 309.00, total 370.80, status mismatch`.

**The line that would have to move:** `evals/extract_invoice/charter.md` lists `status` under Constrained: "`ok` only when the sum of line amounts equals `total` exactly, to the cent. No tolerance." Making a VAT invoice pass means changing that rule, so the check is no longer "lines equal total." That is a moved line, and I'm not allowed to move it or edit the charter myself.

**What moving it would take:**
- A `vat` (or `tax`) field in the extraction. The prompt template is constrained to a fixed text, so the prompt would change too.
- A status rule of "ok when lines + VAT equals total, to the cent," with the VAT computed or read in code.

**What it would buy:** Brightwell and other self-consistent VAT invoices would go to the ledger without a clerk. Real errors, such as a wrong quantity or a mistyped total, would still be flagged, because the total would no longer match the lines plus VAT.

**Options for you to decide:**
1. Amend the charter to allow the VAT check, then I make the change: the prompt gets a VAT field, `status` compares lines + VAT with total, and I add tests for Brightwell and for a mistyped total. This is my recommendation.
2. Keep the rule as it is and accept the clerk load.
3. Loosen the total check with a tolerance. That is also a moved line, and it would hide real errors of a few cents, so I'd advise against it.

Tell me which you want. If it's option 1, the charter needs your edit first, and I'd then agree a spending budget with you before any paid model calls for trials.