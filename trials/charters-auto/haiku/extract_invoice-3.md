# extract_invoice charter

Input: plain text of one supplier invoice (from a PDF or an email), plus a `model` callable (prompt string in, string out).
Output: dict with `supplier`, `invoice_number`, `issue_date` (date), `currency` (3 capitals), `lines` (description, quantity, unit_price, amount), `lines_total`, `total` (Decimal, cents), `status` (`ok` or `mismatch`); or `InvoiceError` naming the field.

## Free
- Reading the invoice: which supplier, number, date, currency, lines and total the text says, across layouts, languages and wording. Fixed rules could not cover every invoice layout.
- Which figure is "the amount due" when the invoice shows several totals (subtotal, VAT, total). Only the model sees the layout; code cannot tell them apart.
- Splitting the invoice into lines and wording each line's description. Code only strips whitespace; no rule could name every line type.
- Converting dates written as "2 Oct 2026" or "02/10/26" into YYYY-MM-DD. The model reads the document's conventions; code only checks the result parses.
- Choosing the currency code from symbols or words ("€", "euros", "EUR"). Code only checks the shape.
- Deriving quantity and unit price when the invoice gives only a line amount. The model reads the invoice; code cannot infer it.

## Constrained
- Number of model calls: exactly one per invoice, no retry, no second pass. Cost and latency scale with calls; a retry would also change which answer is accepted.
- Prompt text: fixed template, with the whole invoice inserted as-is. Keeps the answer format stable and the test that the text reaches the model meaningful. Tightness: exact.
- Empty or whitespace-only text: refused before any model call. Saves a call; there is nothing to read.
- Answer format: the code takes the span from the first `{` to the last `}` and must parse it as a JSON object. Prose and code fences around the object are tolerated; anything else is an error. Tightness: loose on wrapping, strict on JSON. A stray brace in surrounding prose would break parsing.
- Required fields: `supplier`, `invoice_number`, `currency` and `issue_date` must be non-empty strings; `lines` must be a non-empty list; `total` must be a number. Missing means error, not a guess. Checked in this order, first failure wins.
- `issue_date`: must pass `date.fromisoformat`, so only YYYY-MM-DD is accepted. Tight: a date in any other format is refused, not converted.
- `currency`: uppercased, then must be exactly three A–Z letters. Tight on shape, loose on value: any three letters pass, the code does not check against the ISO 4217 list.
- Each line must be an object with numeric `quantity` and `unit_price`. Numbers may arrive as JSON numbers or numeric strings; booleans, non-finite values and non-numeric text are refused. Tight on type. Negative and zero values are not refused.
- `description`: stripped; a missing one becomes an empty string, not an error. Lets a line with no label through to the clerk.
- `supplier` and `invoice_number`: stripped, no format check. Loose.
- Line `amount`: computed by code as quantity × unit_price, rounded to cents with ROUND_HALF_UP. The model's own amount is never read. Keeps the arithmetic checkable; the rounding rule is part of the ledger's expectations.
- `total`: the model's figure, rounded to cents. Code does not read it against the invoice text. The only check is against the lines.
- `status`: `ok` only when the sum of line amounts equals `total` exactly, to the cent. No tolerance. A mismatch is a result, not an error, so the record still reaches a clerk. Tight: a one-cent difference is a mismatch.
- Errors: every refusal raises `InvoiceError` naming the field. The message text is part of the contract, since tests match on it.

## Budget
- Budget: 1 model call per invoice; the full invoice text is sent in one prompt, with no truncation or size limit in code. No timeout, retry or cost cap is set in code; if the model callable has one, it governs. The line count and text length are not capped, so a very long invoice costs more context, not more calls.
