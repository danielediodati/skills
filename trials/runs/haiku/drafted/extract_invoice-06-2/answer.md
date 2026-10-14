I haven't changed the code. The rule that rejects these invoices is a constraint in the charter, and changing it would move a line that only you can move.

**What's happening:** `seam.py` (lines 52–53) requires a numeric `quantity` and `unit_price` on every line, and `evals/extract_invoice/charter.md` lists that as constrained. The Northgate delivery line has only an amount, so the code raises `line 2 quantity is missing`. The IT support fee and the printer's artwork setup fail the same way. A dry run with a fake model reproduced the Northgate error exactly. The 14 existing tests pass.

**Why I didn't make the change:** The obvious fixes all move that line.
- Defaulting a missing quantity to 1 in code is a default, which takes the decision over from the charter.
- Telling the model in `PROMPT` to write quantity 1 for single charges is a prompt that dictates the answer. The prompt wording is also constrained.
- Editing the charter to allow it would be the same move, and that's yours to make.

**What the change would buy:** Single-amount charges (delivery, setup, call-out, annual fees) would load with quantity 1 and unit price equal to the amount. The Northgate invoice would come through as two lines, 285.00 total, `status: ok`, with no retyping. The zero-tolerance total check stays as it is.

**Decision for you:** If you want single-amount lines accepted, update the charter's "Constrained" entry for lines, and I'll implement it (quantity defaulting to 1, plus a test using the Northgate figures). Alternatively, I can leave the rule as it is and you can keep sending those invoices to manual entry. No paid calls were made.