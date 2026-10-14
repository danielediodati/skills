I haven't changed the code. The change you're asking for moves a line the charter holds in code, so it's your decision, not mine.

**What I confirmed**

- The existing 14 unit tests pass.
- Brightwell BP-2291 with the figures you gave comes out as `lines_total 309.00`, `total 370.80`, `status mismatch`. That matches your report.

**Why I stopped**

- `evals/extract_invoice/charter.md` line 26 constrains `status`: it is `ok` only when the line amounts sum to `total` exactly, and the charter says that zero tolerance is deliberate.
- The prompt (`seam.py` lines 10–13) asks for `total` as "the amount due". That figure includes VAT, but the check compares it to net lines. Every invoice with VAT will fail this check, which is why the pile is full of clean invoices.
- Making Brightwell pass needs one of these, and each moves a constrained line:
  1. Add a VAT field to the prompt and change `status` to `lines_total + VAT == total`. Adding a key is a contract change (charter line 18), and the rule change is line 26.
  2. Add a tolerance. The charter rules this out explicitly.
  3. Ask the model to report the net total. That hands a constrained decision to the model.

The charter has no way for the model to supply VAT without changing the fixed prompt, so there is no part of this I can do within the constraints. I haven't edited the charter, and I haven't made any paid model calls.

**What would settle it**

Decide whether you want option 1. If you do, update the charter yourself: the VAT key, whether VAT is checked against the rate or only as a sum, and what a VAT mismatch does. Once the charter says so, I can make the code and test changes. The Brightwell case should become a test: `lines 309.00 + VAT 61.80 = total 370.80` gives `ok`, and a mistyped total still gives `mismatch`.