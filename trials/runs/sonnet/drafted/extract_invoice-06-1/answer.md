I changed the prompt so the model reports a single-amount charge as quantity 1 at that amount. I have not checked that a real model now does this on invoices like NF-0718.

**What I changed**
- `seam.py`: the prompt now says every line needs both `quantity` and `unit_price`. A charge printed as a single amount, such as a delivery charge or flat fee, gets `quantity` 1 and that amount as `unit_price`.
- `test.py`: two new tests. One checks the prompt carries that guidance. The other loads the Northgate shape (40 × 6.25 plus delivery 35.00, total 285.00) and gets two lines, a lines total of 285.00 and status `ok`.
- All 16 local tests pass. They use a fake model, so they don't show what a real model does with the new wording.

**What I did not do**
Making the code default a missing quantity to 1 would have fixed this deterministically. The charter forbids it: "A missing or unreadable number is an error and is never defaulted to 0 or 1." That rule is there so a wrong ledger entry is never silently created. Moving it is your call, not mine. If you want it, you would need to change the charter. A narrower rule is possible, such as defaulting only when the model gives a unit price and no quantity. I'd recommend keeping the prompt-only fix unless the real-model check shows it fails.

**Next step**
To confirm a real model now returns a quantity for these lines, I'd run a small check on the three invoices you mentioned (Northgate, the IT support fee, the printer setup fee). That is paid, so I need your approval, and we should agree a spending budget for this ticket first. A few calls would be enough. Tell me the model and the budget you want, and I'll run it.