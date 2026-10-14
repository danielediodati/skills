I couldn't make this change without moving a line in the seam's charter, so I've left the code alone. The failure reproduces locally, and the existing 14 tests pass.

**The line in question** is in `evals/extract_invoice/charter.md`, under Constrained:

> quantity and unit_price: must be present, not boolean, and parse as finite decimals (numbers or numeric strings)

The total has the same kind of rule ("must be a present finite number"). `seam.py` `_number()` uses `Decimal(str(value))`, which rejects `1.250,00` and `2.340,50`. To accept them, the code would need a rule for how to read locale-formatted strings. Adding that rule loosens what the charter says the code accepts, so it's the user's call and I haven't changed it.

**The other route also moves a line.** The charter leaves decimal style to the model under Free ("the model chooses, as long as the code can parse it"). Changing `PROMPT` to ask for dot-decimal numbers would take that choice away from the model, so that route needs the same decision.

**Reproduction** (fake model, no paid calls):
- Kessler, unit_price `'1.250,00'` → `InvoiceError: line 1 unit_price is not a number: '1.250,00'`
- Cartiera Lombarda, unit_price `'2.340,50'` → `InvoiceError: line 1 unit_price is not a number: '2.340,50'`

I haven't tested the real model's output for these invoices, and I haven't run any paid calls.

**Decisions for you, to amend the charter if you want this:**
1. Allow locale-formatted numeric strings in `quantity`, `unit_price` and `total`. The rule needs to say what `1.250` means, since a German reader takes it as 1250 and an English reader as 1.25. A reasonable rule: if both `.` and `,` appear, the last one is the decimal mark. If only one appears, treat it as a decimal mark only when followed by one or two digits and as a thousands separator when followed by exactly three. Please confirm or give another rule.
2. Keep the model's choice of format free, and let the code parse what it writes. This is the reading I'd recommend, since it matches the Free line about decimal style.

Once you've amended the charter, I'll add the parser to `seam.py`, add tests for `1.250,00`, `2.340,50` and the ambiguous cases, and run the suite. I'd also suggest one paid run on the Kessler invoice, which would need your approval for the budget first.