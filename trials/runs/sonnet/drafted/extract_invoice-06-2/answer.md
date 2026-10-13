I changed the prompt so a single-amount charge like the Northgate delivery line should now load, but I haven't confirmed that against a real model. The 16 unit tests pass, but they use a fake model, so they can't show how a live model reads these invoices.

**Cause.** The model was reading "Delivery — 35.00" as a line with no quantity. The code correctly refused it, because the charter says a missing value is never defaulted.

**Change.** In `seam.py`, the prompt now tells the model that a charge printed as a single amount (delivery, setup fee, annual support fee) has no quantity or unit price on the invoice. It should report that charge as one line with quantity 1 and unit_price equal to the amount.

- **What stays with the model:** it still decides which lines are such charges and what each line's values are.
- **What stays in code:** the missing-quantity check, the line amounts, the exact-equality status and the rounding are untouched. Code does not default quantity to 1, since that would have moved a constrained line.

**Tests.** I added two to `test.py`: the prompt carries the guidance, and an invoice with a 40 × 6.25 line plus a 1 × 35.00 delivery line totals 285.00 with status `ok`.

**Not done.** To confirm a live model gets this right, I'd run the NF-0718 text, the IT contractor's "Annual support fee — 1,200.00" and the printer's "Artwork setup — 60.00" through the real model, one call each. Nothing paid has run, so there is no spending budget yet. If you want this check, tell me a budget and which model to use.