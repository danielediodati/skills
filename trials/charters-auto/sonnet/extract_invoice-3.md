# extract_invoice charter

Input: the plain text of one supplier invoice (from a PDF or email), plus a model callable (prompt string in, string out).
Output: a dict with supplier, invoice_number, issue_date (`date`), currency, lines (description, quantity, unit_price, computed amount), lines_total, total (all `Decimal` in cents) and status `ok`/`mismatch`; or `InvoiceError` naming the field.

## Free
- Reading the invoice: which text is the supplier, invoice number, issue date, currency, each line and the amount due; invoice layouts and wording are too varied for rules, so the model interprets them.
- Normalising the date and the currency to YYYY-MM-DD and a three-letter code: the invoice text states them in many formats ("2 Oct 2026", "€"), and the model is asked to convert them.
- Splitting the invoice into lines and choosing each line's description, quantity and unit_price: what counts as a line (versus a subtotal, tax or note) depends on the layout and is judged by the model.
- Which figure is "the total" (the amount due): the model picks it from the text; code only compares it against the lines afterwards.
- Wrapping the answer: the model may add a code fence or a sentence around the JSON; code tolerates that rather than requiring a bare object.

## Constrained
- Empty or blank text is refused with `InvoiceError` before the model is called: nothing can be extracted, and it saves a call.
- One model call, no retry or repair: an unreadable answer raises instead of being re-asked, so failures are visible and cost stays fixed (today's choice; a retry could be added without breaking the contract).
- JSON is located from the first `{` to the last `}` and must parse to an object: lenient on wrapping only; anything else is `InvoiceError` "not JSON".
- Required fields (supplier, invoice_number, issue_date, currency, at least one line, total, each line's quantity and unit_price) must be present and valid, otherwise `InvoiceError` naming the field: a half-filled record must never reach the ledger, and a missing value is never guessed or defaulted. Only a line description may be absent (becomes an empty string).
- issue_date must parse as an ISO date and currency must match three letters A-Z after upper-casing: format is checked in code; the model's value is not trusted. The date is not checked for plausibility and the currency is not checked against a list of real codes.
- Numbers are parsed as `Decimal` (never float), must be finite, and booleans are refused: money arithmetic must be exact.
- Line amount = quantity × unit_price, computed by code and rounded half-up to cents; the model's own line amounts are not requested or used: arithmetic is deterministic and checkable, and the model is unreliable at it.
- lines_total is the sum of the computed line amounts, and total is rounded to cents the same way: both sides of the comparison use the same rounding.
- Status is `ok` only if lines_total equals total exactly (zero tolerance), else `mismatch`: the check that routes an invoice to a clerk is fixed in code and is not left to the model. A mismatch is returned, not raised, and the model's total is never "corrected" to the lines.
- Output shape, keys and types are fixed (supplier and invoice number stripped of whitespace, `date`, `Decimal`); the ledger loader depends on them.
- The prompt fixes the requested keys and asks for JSON only; the invoice text is passed in whole, with no truncation.

## Budget
- Budget: one model call per invoice; no latency or cost limit is set in code. The whole invoice text goes in the prompt, with no length cap.
