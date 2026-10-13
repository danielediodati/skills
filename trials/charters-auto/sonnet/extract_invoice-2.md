# extract_invoice charter

Input: the plain text of one supplier invoice (from a PDF or an email), and a model callable (prompt string in, string out).
Output: a dict with supplier, invoice_number, issue_date (`date`), currency, lines (description, quantity, unit_price, computed amount), lines_total, total (all `Decimal`, cents) and status `ok`/`mismatch`; or an `InvoiceError` naming the field.

## Free
- Reading the invoice layout: which text is the supplier, the invoice number, the issue date, the currency, each line and the amount due, across any layout, language or wording; code cannot parse unforeseen invoice formats.
- Normalising what it read: turning "2 Oct 2026" into YYYY-MM-DD, a symbol or name into a currency code, "1.234,50" into a number; the prompt asks for this and code only checks the result.
- Which text counts as an invoice line, and what each line's description, quantity and unit_price are; code sees only the model's list.
- Which figure is "the total" (the amount due); the model picks it from the text, and code only compares it with the lines.
- The wording of the answer around the JSON: prose or a code fence is tolerated, so the model need not be perfectly terse.

## Constrained
- Whether the text is worth a model call: blank text is refused before the model is asked, to save a call that cannot succeed.
- Output shape: the model must answer with one JSON object, taken from the first `{` to the last `}`; anything else raises `InvoiceError("... not JSON")`. Code never guesses or repairs a missing answer, so no half-read record reaches the ledger.
- Required fields: supplier, invoice_number, issue_date, currency and total must be present and non-blank, and there must be at least one line; otherwise `InvoiceError` names the field. A missing value is never defaulted, because a silent default would enter the ledger unnoticed.
- Dates: must be ISO `YYYY-MM-DD` and a real calendar date; nothing else is accepted, and no plausibility check (future, old) is made.
- Currency: upper-cased and must be exactly three letters A-Z; it is not checked against the ISO 4217 list.
- Numbers: quantity, unit_price and total must parse as finite `Decimal` (booleans and null rejected); parsed from the string form to avoid float error. Negative values and zero are accepted (credit notes).
- Line description: optional; blank is allowed and trimmed.
- Money arithmetic: line `amount` = quantity × unit_price, computed by code and rounded half-up to cents per line; the model never supplies amounts. Reason: the model's arithmetic is not trusted and the rounding rule must be reproducible.
- `lines_total` is the sum of the rounded line amounts; `total` is rounded half-up to cents.
- Status: `ok` only if `lines_total == total` exactly, with no tolerance; otherwise `mismatch`. This is a decision in code, not the model's judgement, so a mismatched invoice goes to a clerk and never to the ledger.
- A mismatch is a result, not an error: the record is returned in full with status `mismatch`, so the clerk can see both figures. Only unreadable or malformed answers raise.
- No retry and no second opinion: a bad answer fails at once with `InvoiceError`; the caller decides what to do.
- Model contract: the model is injected as a plain callable, so the seam stays testable without a live model.

## Budget
- Budget: exactly one model call per invoice, no retries; the prompt contains the full invoice text, with no truncation or size cap. The single call is a design choice (cheap, predictable), not a measured limit; the exact-equality status check and half-up cent rounding are the constraint itself, not a tunable budget.
