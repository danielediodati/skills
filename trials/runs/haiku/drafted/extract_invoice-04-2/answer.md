Invoices whose amounts are written with German or Italian separators now load with the right figures. The Kessler total `1.250,00` reads as 1250.00, and the Cartiera unit price `2.340,50` reads as 2340.50. All 18 tests pass, including four new ones.

**What changed**

- `seam.py`: `_number` now passes values through a new `_plain_decimal` helper before parsing. The helper treats the separator written last as the decimal mark and drops the other one. A lone comma counts as a decimal mark only when one or two digits follow it.
- `test.py`: new tests for German amounts, Italian amounts, English thousands (`1,250.00`), and the ambiguous `1,250`, which is still refused.

**Where the line sits**

I took the reading that number notation is part of the code's constrained parse, so the change stays in code. I did not change the prompt, because asking the model to normalise numbers would hand that interpretation to the model. I did not edit `evals/extract_invoice/charter.md`. The charter says the total is "parsed as a number" but doesn't say how locale notation is handled, so you may want to add a line about it there.

**Limits to know about**

- `1.250` with a single dot is still read as 1.25, as it was before. A German "1.250" meaning 1250 would therefore still load silently wrong. Refusing three-digit groups after a lone dot would fix this, but it tightens existing behaviour, so I left it for you to decide.
- Space-grouped thousands (`1 250,00`, common in French) are not handled.
- I haven't run the real Kessler or Cartiera invoices through the model. Nothing paid was run, and I don't have the invoice text. The parser checks above used the exact amount strings from the report.

This is not a git repository, so I didn't commit anything.