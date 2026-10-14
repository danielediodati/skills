Nothing is changed yet. The fix needs a charter line moved, so I stopped before editing code.

**What's stuck:** The model returns the amount as the invoice prints it (`"1.250,00"`), and `seam.py` refuses that text because `Decimal` can't read it. Both rejections you described come from this check: `total` at `seam.py:61` and `unit_price` at `seam.py:53`, through `_number` at `seam.py:94`. I reproduced both messages. The existing 14 tests pass.

**The lines I'd have to move** (`evals/extract_invoice/charter.md`):
- **Line 22 (types):** "Numbers may arrive as JSON numbers or numeric strings … non-numeric text is refused. Tight on type." Reading `1.250,00` as 1250.00 widens what counts as a numeric string, so it loosens this check.
- **Line 16 (prompt):** the prompt is a "fixed template … Tightness: exact." Asking the model for plain decimal numbers means changing that template.

**Options (the decision is yours):**
1. **Model normalizes the numbers.** Add an instruction to the prompt to output `total` and line prices as plain numbers with a `.` decimal point and no thousands separator. This matches how the charter already treats dates (line 10): the model reads the document's conventions, and code only checks that the result parses. It moves the prompt line. It also depends on the model complying, and I can't check that without a paid call.
2. **Code parses locale numbers.** Accept `1.250,00` and `2.340,50` in `_number`. This moves the type line. It also has an ambiguity problem: `1.250` means 1250 in German and 1.25 in English, so the code would have to guess, and the charter gives the reading of conventions to the model. A safer version would send single-separator cases like that to a clerk rather than guess.

My recommendation is option 1, since it matches the date rule already in the charter. Either way, the change needs your approval to edit the charter or the prompt. Once you approve one, I can make the code side and add tests. Any check against the real model would be a paid call, so I'd agree a budget with you before running it.