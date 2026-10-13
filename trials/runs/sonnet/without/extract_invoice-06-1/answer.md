Invoices with a flat charge, like the Northgate delivery line, now load as normal instead of failing with `line 2 quantity is missing`. The tests pass, including three new ones; I haven't run it against a real model.

**What changed**
- **Reading the line (`seam.py`):** a line with no `quantity` and no `unit_price` but an `amount` is read as quantity 1 at that amount. For NF-0718 the delivery becomes `1 × 35.00 = 35.00`, the lines total 285.00, and the status is `ok`.
- **Instructions to the model (`seam.py`):** the prompt now tells the model to return such a line with `quantity` and `unit_price` null and the printed figure as `amount`. Without this the model would have nothing to put in the line, and the fix would never trigger.
- **README and tests:** the README describes the behaviour. The new tests cover the Northgate shape, a flat line with the keys left out entirely (the annual support fee), and a line with only a description, which stays an error.

**Behaviour to know about**
- A line with only one of `quantity` or `unit_price` is still rejected, as before. A lone figure there is ambiguous, and guessing could put a wrong amount in the ledger.
- The existing total check is unchanged, so an invoice whose lines don't add up still comes back as `mismatch` for a clerk.