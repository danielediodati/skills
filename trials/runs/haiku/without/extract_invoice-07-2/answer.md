Ambiguous invoice dates now raise an error for a clerk instead of being guessed. The 23 unit tests pass, including the Brightwell case.

**What was wrong:** the model was asked for `issue_date` in `YYYY-MM-DD`, so it decided whether "05/08/2026" was day-first or month-first, and nothing checked that choice.

**What changed in `seam.py`:**
- The model now copies the date exactly as printed (`issue_date_as_printed`). The code parses it.
- Dates that only one reading makes valid are accepted: "13/08/2026", "2026-08-05", "5 Aug 2026".
- Dates that fit both readings need a `date_order` argument, `"DMY"` or `"MDY"`. With that set, "05/08/2026" becomes 5 August 2026 for Brightwell and 3 April becomes 4 March for the American supplier.
- With no `date_order`, the invoice raises `InvoiceError` ("issue_date is ambiguous") and goes to a clerk. No date is guessed.
- Impossible dates such as 31/02 are rejected.

**Choices I made that you may want to change:**
- I put the date order on the supplier, not the invoice, because the invoice's own format is the thing that can't be trusted. The code does not read it from the supplier record; your accounts-payable system has to pass `date_order` in. If the supplier record has no date-format field, every ambiguous numeric date will go to a clerk until one is added.
- Two-digit years and dates written without a year are rejected, not parsed.

**Also changed:** the tests now use the new field name and cover the cases above. `README.md` describes the new argument and behaviour. The project is not a git repository, so nothing was committed.