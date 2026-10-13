I haven't changed anything, because fixing this means moving a line the charter holds in code, and only you can do that.

**The line.** `evals/extract_invoice/charter.md` makes the status rule a constrained decision. Status is `ok` only when `lines_total` equals `total` exactly, with no tolerance, because that rule decides routing to a clerk. The charter also records your case explicitly: "a VAT invoice reports `mismatch` (it goes to a clerk). Assumed." So BP-2291 is routed this way by design. The tool reads 309.00 for the lines and 370.80 for the amount due, and they differ.

**Why every way of meeting the request crosses it:**
- **Accept lines + VAT = total:** this changes the rule from "lines equal total" to "lines plus tax equal total". That redefines what `ok` means.
- **Tell the model to report the net figure as the total:** this makes the prompt dictate the answer to the check. It also contradicts the charter's definition of `total` as the amount due.
- **Loosen the comparison with a tolerance or a 20% allowance:** the charter rules out tolerance, and it would let real errors through.

**What moving it would buy.** Correct VAT invoices would go straight to the ledger, and the review pile would hold only invoices where the figures really disagree. The risk is that a rule that accepts tax now depends on a figure the model read (the tax amount). A misread tax line could make a wrong invoice look consistent, so the charter would need to say how that figure is read and checked.

**A design you could approve.** Have the model also report the tax amount (or amounts) as printed. Code would then set `ok` when `lines_total + tax == total` exactly, and `mismatch` otherwise. It would still never correct either figure. The charter would need to record the tax figure as a free reading and the new equality as the constrained rule.

If you want that, update the charter (or tell me the wording you want and I'll implement it once you've changed it). I can then make the code, prompt and tests follow.