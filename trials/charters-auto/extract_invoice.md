# extract_invoice charter

Input: the plain text of one supplier invoice (from a PDF or an email), and a model callable (prompt string in, string out).
Output: a dict with supplier, invoice number, issue date (`date`), currency, lines (description, quantity, unit_price, computed amount), lines_total, total (all `Decimal`, cents) and `status` `ok`/`mismatch`; or an `InvoiceError` naming the field.

## Free
- Reading the layout: which text is the supplier, the invoice number, the issue date, the currency, each line and the amount due. Invoices come in every format, and this is the work the model is there for.
- Normalising the date to YYYY-MM-DD from whatever form the invoice uses ("2 Oct 2026"): the model reads the many written forms; code only checks the result.
- Which figure is "the total" (the amount due) and which rows are invoice lines rather than subtotals, tax, notes or page footers: this takes judgement about the document. Code only compares what the model chose.
- Line descriptions: free text, kept as the model wrote it (only stripped); an empty description is accepted because nothing downstream depends on it.
- Whether the answer is wrapped in a fence or a sentence, and the number form (JSON number or string) of quantity, unit_price and total: code tolerates both, so the model's style is free.

## Constrained
- One model call per invoice, no retry or repair loop: a bad answer is an error for a person to see, not something to ask again (cost, latency, deterministic behaviour). Today's choice; the tests pin one prompt per call.
- Empty or whitespace-only text is refused before the model is called: nothing to read, and the call would be wasted (pinned by a test).
- Output shape asked of the model is fixed in the prompt: JSON only, the six keys, ISO date, three-letter currency. Code depends on these exact key names.
- JSON is taken from the first `{` to the last `}`: tolerates fences and chatter, but anything not a JSON object is `InvoiceError("... not JSON")`.
- Required fields (supplier, invoice_number, issue_date, currency) must be non-empty strings; missing means `InvoiceError`, never a guessed or default value. A wrong ledger entry costs more than a refused one.
- issue_date must parse as an ISO date. There is no plausibility check (future or old dates are accepted).
- currency is upper-cased and must be exactly three letters A-Z. It is not checked against the ISO 4217 list, and no currency is ever defaulted.
- At least one line is required, and each line must be an object with numeric quantity and unit_price; description may be absent. Quantity and price signs are not checked, so credit lines pass.
- Numbers must be finite and parse as `Decimal` (booleans and null are refused): money is never a float, and "not a number" is an error naming the field.
- Line amount is computed by code as quantity x unit_price, rounded half-up to cents per line; the model's own arithmetic is never used. lines_total is the sum of the rounded line amounts. Rounding per line is the rule that matches how ledgers post lines (pinned by the 0.335 test).
- Total is rounded half-up to cents.
- Status is decided by code with exact equality of lines_total and total, with no tolerance. It never raises: `mismatch` is a valid result that routes the invoice to a clerk instead of the ledger. This is the safety check on the model's reading; if it moved to the model, a model that misread would also vouch for itself.
- Nothing is verified against the invoice text (supplier, number and figures are trusted as the model reported them, short of the checks above); the only cross-check is total versus lines.
- Error messages name the field (`supplier is missing`, `line 1 quantity is missing`): callers and tests rely on them.

## Target and budget
- Budget: one model call and no retry per invoice; code work is negligible. The invoice text goes into the prompt whole, with no truncation or size cap, so context size is the model's limit.
- The exact-equality tolerance (zero cents) is a deliberate constraint, not a tunable budget. Invoices whose total includes tax or shipping that is not a line will show as `mismatch` by design.
