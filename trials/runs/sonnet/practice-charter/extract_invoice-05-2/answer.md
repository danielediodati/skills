I haven't changed anything. Fixing this means moving a line that the charter reserves to you, so the decision is yours.

**Why Brightwell goes to a clerk.** `evals/extract_invoice/charter.md` says status is `ok` only when `lines_total` equals `total` exactly, with no tolerance. It also records, as an assumption, that a VAT invoice reports `mismatch`. For BP-2291 the lines come to 309.00 and the amount due is 370.80, so the invoice is marked `mismatch`. This is what the rule says, not a bug.

**The line.** It sits in the charter's Constrained section: "Status is `ok` only on exact equality of lines_total and total" and "Invoices with tax, discount or shipping rows outside the lines… reports `mismatch`". Any fix changes how status is decided, and that rule exists so routing is identical on every call.

**What moving it would buy.** I see two ways, and I recommend the first:

1. **Extract the tax and let code check it.** The model reads the VAT amount as a new field. This is a reading task, so it fits the Free section. Code would then compute `ok` when `lines_total + tax == total` exactly, still with no tolerance.
   - BP-2291 passes: 309.00 + 61.80 = 370.80.
   - A wrong quantity or a mistyped total still fails, because the arithmetic stays exact and in code.
   - The cost is that a wrongly read VAT figure could hide a real error. It would have to coincidentally make the sum work, which is unlikely.
2. **Have the model report the net total instead of the amount due.** I advise against this. It hands the model a figure that the check depends on, and it stops the check from verifying the amount that actually gets paid.

**What I need from you.** Update the charter so the status rule and the VAT assumption reflect option 1, or tell me you prefer something else. Once the charter says so, I'll make these changes:

- Add `tax` to the prompt and the record.
- Change the status rule to include tax.
- Update the tests, including a BP-2291 case with VAT and a case where a wrong figure still yields `mismatch`.

I could also add the extracted tax to the record for clerks to see while leaving status as it is. That wouldn't empty the review pile, so I haven't done it.