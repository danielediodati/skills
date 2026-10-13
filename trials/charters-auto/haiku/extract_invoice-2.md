# extract_invoice charter

Input: plain text of one supplier invoice (from a PDF or email), plus a `model` callable that takes a prompt string and returns a string.
Output: dict with `supplier`, `invoice_number`, `issue_date` (date), `currency`, `lines` (description, quantity, unit_price, amount), `lines_total`, `total` (Decimal to cents), `status` (`ok` or `mismatch`); or `InvoiceError` naming the failing field.

## Free
- Reading the invoice: which text is the supplier, invoice number, date, lines and amount due; invoice layouts and languages vary, so the model finds them.
- Supplier and invoice number wording: the model copies them from the document; code only requires a non-empty string and strips whitespace, so unusual but real identifiers pass.
- Line description wording: the model writes it; code strips it, and a missing description becomes "" instead of an error, because the amount does not depend on it.
- Which numbers count as quantity and unit price (e.g. discounts, tax lines, units): the prompt does not say, so the model decides and code only checks that each is a finite number.
- Date format as read: the model converts to a date string; code validates the result rather than dictating how it was found.
- Currency choice: the model picks the code from the invoice; code only checks its shape.
- The amount due: the model decides which figure is the total; code takes it as given and checks it only against the lines.
- Prose or code fences around the answer: the model may add them, since code cuts the answer to the first `{` through the last `}`.

## Constrained
- Empty or whitespace-only text: refused before the model is called, to avoid paying for a call that cannot produce an invoice.
- Prompt wording and keys: fixed in `PROMPT`, so the answer shape is the same for every invoice and the parser can rely on it. Changing a key is a contract change.
- Answer must contain a JSON object: parsed by code; anything else raises "not JSON" or "not a JSON object", because nothing downstream can use it. No retry.
- Required fields `supplier`, `invoice_number`, `issue_date`, `currency`, `total`, `lines`: each must be present; missing or blank raises an error naming the field. These are the minimum a ledger entry needs.
- `issue_date`: must be a real calendar date accepted by `date.fromisoformat` (strict ISO format on Python 3.10; 3.11+ accepts a few more ISO forms). Dates like "2nd October" or 30 February are refused, because a wrong date posts to the wrong period.
- `currency`: uppercased, then must be exactly three A–Z letters; not checked against the ISO 4217 list, so an unreal code such as "XXX" passes. Tight on shape, loose on membership.
- `lines`: must be a non-empty list of objects; each needs numeric `quantity` and `unit_price` (booleans and non-finite values refused). Sign and magnitude are not checked, so negative or zero values pass. No cap on the number of lines.
- Line `amount`: quantity × unit_price, rounded to cents half-up; computed by code, never by the model, so the arithmetic is exact and repeatable. `quantity` and `unit_price` are kept unrounded.
- `total`: parsed as a number and rounded to cents half-up, so every money value in the ledger has the same precision.
- `status`: `ok` only when the sum of rounded line amounts equals `total` exactly; otherwise `mismatch`. Zero tolerance is the constraint itself: any tolerance would let a wrong amount reach the ledger. A mismatch is a result, not an error, so the invoice still returns and goes to a clerk.
- Failure handling: any invalid answer raises `InvoiceError`; no fallback value, no partial record, no second model call. The caller decides what happens next.

## Budget
- Budget: exactly 1 model call per invoice, 0 for empty text. The single call is a structural choice in the code, not a tunable number; no retry exists.
- Context: the whole invoice text is inserted into the prompt with no truncation or length cap; long invoices are sent in full.
- Seconds and cost: none set in code; they depend entirely on the model supplied by the caller.
