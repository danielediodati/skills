I haven't changed anything. Fixing this means moving a line the charter holds in code, and only you can move it.

**Why Brightwell is flagged.** `seam.py:71` sets status to `ok` only when `lines_total == total`. For BP-2291 that compares 309.00 with 370.80, so it returns `mismatch`. The charter makes this deliberate, in two places in `evals/extract_invoice/charter.md`:

- **Line 19:** status is `ok` only on exact equality of lines and total, with no tolerance, so routing is identical on every call.
- **Line 25:** invoices with tax rows outside the lines report `mismatch` and go to a clerk. It is marked "Assumed", which is why your VAT invoices land in the review pile.

**What moving the line would buy.** Under the current rule, "consistent" can only mean lines equal total. To let a VAT invoice through, the check has to become lines + tax = total. That needs two things:

1. The model reads the tax amount off the page. This is a reading task, so it fits the model's side of the charter.
2. Code checks `lines_total + tax == total` exactly and sets status from that. This replaces the rule at line 19, and the status stays computed by code and never taken from the model.

**Decision for you.** Do you want the status rule changed to `lines_total + tax == total`, still exact and still computed in code? If so, you'd need to update charter lines 19 and 25 yourself, since I'm not allowed to edit the charter. After that I'd make the code, prompt and test changes. The Brightwell figures would then give 309.00 + 61.80 = 370.80, which is `ok`.

There is a risk to weigh. The tax figure comes from the model, so a misread tax could make a wrong total look consistent. The code could limit this by also requiring that tax is non-negative, and you could add a rate check if you want it stricter.