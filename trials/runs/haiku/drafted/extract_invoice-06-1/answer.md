I haven't changed the code. The rule that rejects these lines is one the charter places in code, and meeting your request means moving that line, which only you can decide.

**What I checked**
- The 14 existing tests pass.
- I reproduced the Northgate failure with a fake model, which makes no paid call. The answer for NF-0718 gives `InvoiceError: line 2 quantity is missing`.

**Where the line is**
- `evals/extract_invoice/charter.md`, Constrained section: "quantity and unit_price: must be present". The check is at `seam.py:52`.
- `test.py:103` (`test_missing_quantity_is_an_error`) pins that rule.

**Why I stopped**
Every route I can see that loads these invoices moves that line:
1. **Code default:** treat a missing quantity as 1 at `seam.py:52`. This loosens a constrained check.
2. **Prompt change:** tell the model to write `"quantity": 1` for a single charge. The charter lists prompt wording as fixed, and this would make the model supply a constrained field.

Either way the charter has to change first, and I won't edit the charter. There is no part of the request I can finish without moving that line, so I made no edits.

**What moving the line would buy**
Single-amount lines like "Delivery — 35.00" would load as a line with quantity 1. Northgate would come through with two lines and a total of 285.00. The line-sum check against the printed total stays, so a wrong delivery amount would still come out as `mismatch` and go to a clerk.

**Decision for you**
If you want this, update the charter's quantity rule first. Say whether a missing quantity should default to 1 in code, or whether only a line with a unit price and no quantity should qualify. Once the charter says so, I'll make the code change and update `test_missing_quantity_is_an_error` to match.