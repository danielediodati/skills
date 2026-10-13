# extract_invoice charter

Input: plain text of one supplier invoice (from a PDF or email), plus a model callable that takes a prompt string and returns a string.
Output: dict with supplier, invoice_number, issue_date (date), currency, lines (description, quantity, unit_price, amount), lines_total, total (Decimal, cents) and status (ok or mismatch); or InvoiceError naming the field.

## Free
- Reading the invoice: which text is the supplier, invoice number, date, currency, lines and total; the model handles any layout, language or wording, which code cannot anticipate.
- Which printed rows count as invoice lines (delivery, fees, discounts, tax): the model judges the document; code only sums whatever lines it returns.
- Which figure is the total: the model picks the "amount due" as printed; code does not know whether tax or shipping is included.
- Line descriptions: the model writes them; code only strips whitespace.
- Date and currency spelling in the source: the model normalises "2 Oct 2026" to YYYY-MM-DD and "euros" or "€" to a code, because only it can read the varied source.
- How numbers are written in the answer (number or string, decimal style): the model chooses, as long as the code can parse it (see Constrained).
- Surrounding prose or code fences around the JSON: the model may add them, because models often do; code extracts the object.

## Constrained
- Empty or whitespace-only text: refused before the model is called, because there is nothing to read and a call would waste budget.
- Prompt wording and schema keys: fixed in the PROMPT constant, so every invoice is asked the same question and answers keep the same shape.
- JSON location: the code takes the text from the first "{" to the last "}" and must parse it as a JSON object; no other format is accepted, so the ledger never receives a list or bare value.
- Required text fields (supplier, invoice_number, issue_date, currency): must be non-empty strings, stripped; a missing one is refused, because each is needed for the ledger record.
- issue_date: must parse as an ISO date via date.fromisoformat; tight, because the ledger stores a real date and a wrong one would misfile the invoice. Python's parser also accepts compact forms such as 20261002, which the code does not reject.
- currency: uppercased, then must be exactly three letters A-Z; this checks shape only, not membership in ISO 4217, so an unknown but well-formed code passes.
- lines: must be a non-empty list of objects; no maximum count is set, so a very long invoice is accepted.
- description: optional; a missing one becomes an empty string rather than an error, a looser rule than the other fields.
- quantity and unit_price: must be present, not boolean, and parse as finite decimals (numbers or numeric strings); there is no sign or range check, so negative or zero values pass.
- amount per line: computed by code as quantity times unit_price, rounded half-up to cents; the model never supplies it, so the arithmetic is fixed and reproducible.
- total: must be a present finite number, rounded half-up to cents; the printed total is taken as the reference the lines are checked against.
- lines_total: the sum of the rounded line amounts, computed by code.
- status: "ok" only when lines_total equals total exactly in cents; there is no tolerance, so any cent difference is a mismatch. This is the line that routes an invoice to a clerk, and it must not be moved to the model, which could approve a bad total.
- Retry: none; the model is asked once and a bad answer raises InvoiceError, so the caller decides what to do.
- Errors: every refusal is InvoiceError with a message naming the field, so the caller can report which field failed.

## Budget
- Budget: 1 model call per invoice, no retries; no timeout, token limit or cost cap in code; the whole invoice text is sent with no truncation, so it must fit the model's context window.
