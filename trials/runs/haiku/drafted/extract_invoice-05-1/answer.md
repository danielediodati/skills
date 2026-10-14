I haven't changed anything. Making the Brightwell invoice pass would mean changing the rule that decides `ok` or `mismatch`, and the charter puts that rule under the user's control.

**What I checked**
- The existing suite passes: 14 tests, OK.
- With the Brightwell figures run through a fake model (no paid calls), the tool gives `lines_total 309.00`, `total 370.80`, `status mismatch`. That matches your report. The cause is that the VAT row isn't in the lines and the status check compares the lines against the VAT-inclusive total.

**The line that stops me**
- `evals/extract_invoice/charter.md`, Constrained, `status`: "ok only when lines_total equals total exactly in cents; there is no tolerance … it must not be moved to the model."
- `seam.py:71` implements this: `"ok" if lines_total == total else "mismatch"`.
- Passing a VAT-inclusive invoice means `ok` has to mean "lines plus VAT equals total". That changes the check, and the charter says only you change it.

**What I left alone**
- I didn't edit `seam.py`, the charter, or the tests.
- I didn't make a paid model call.
- Asking the model to list VAT as a line would also be a change: the prompt is a constrained item, and the charter leaves it to the model to decide whether tax rows count as lines. I wouldn't do that without your decision.

**Options for you to decide**
1. **Code-side VAT check (recommended if you want the Brightwell case to pass).** Add a constrained `vat` field to the schema (printed VAT amount, or none), and make `status` ok when `lines_total + vat == total` exactly in cents. Lines without VAT keep today's behaviour, and a mistyped quantity or total still goes to the clerk. You'd need to amend the charter's `status` entry to match, and that's your call.
2. **Keep the rule and accept VAT-inclusive invoices going to review.** This changes nothing, but the pile stays as it is.

Which do you want? If you pick option 1, I'll make the code change and the tests once the charter is updated, and I'll check the Brightwell case and a mistyped-total case with the free local tests before any paid run.