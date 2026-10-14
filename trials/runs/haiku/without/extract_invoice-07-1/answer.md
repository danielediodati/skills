The date parsing now happens in code rather than in the model's head, and an ambiguous date stops the invoice instead of going into the ledger. All 24 tests pass (`python -m unittest`).

**What was wrong:** `seam.py` asked the model to convert the printed date to ISO format itself. Nothing checked how it read `05/08/2026`, so the day and month could be swapped without any sign.

**What changed in `seam.py`:**
- The model now copies the date exactly as printed. The code reads it.
- `extract_invoice` takes a new optional `date_orders` mapping: supplier name → `"DMY"` or `"MDY"`.
- A numeric date is resolved as follows:
  - If one part is over 12, that part must be the day, so the order is settled by the numbers.
  - If both parts are the same, the date is the same either way.
  - Otherwise the supplier's order from `date_orders` is used.
  - If neither settles it, the function raises `InvoiceError` ("issue_date is ambiguous"), and the invoice goes to a clerk.
- Written-out dates ("5 August 2026") and ISO dates have one reading and need no order.
- Impossible dates such as 31/02 are rejected.

**Tests:** I added cases for BP-2304 (`05/08/2026` for Brightwell → 5 August 2026), the US invoice (`03/04/2026` for a month-first supplier → 4 March), an ambiguous date with no order on file, and a few others. The README documents the new parameter.

**Choices I made that you may want to change:**
- The order table is a plain dict passed in by the caller. I didn't invent a supplier list. Someone needs to maintain it, and Brightwell must be entered as `"DMY"` for the fix to load it correctly.
- The supplier is matched on the exact name as printed. A variant spelling ("Brightwell Paper Limited") is treated as unknown and sent to a clerk. That is deliberate, but it means the table needs every spelling that appears on invoices.

**Not done:**
- I did not touch any ledger data. BP-2304 and the US invoice are already loaded with the wrong dates, so they need correcting by hand.
- This folder isn't a git repository, so I did not commit anything.
- One possible extra guard: check that the date string the model returned actually appears in the invoice text. That would catch the model mis-copying the date. I haven't added it, since you didn't ask for it.