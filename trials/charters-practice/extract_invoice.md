# extract_invoice charter

Input: the plain text of one supplier invoice (from a PDF or email), and a model callable (prompt string in, string out).
Output: a dict with supplier, invoice_number, issue_date (date), currency (3 capitals), lines (description, quantity, unit_price, computed amount), lines_total, total (Decimal, cents) and status `ok`/`mismatch`; or `InvoiceError` naming the field.

## Free
- Which figures on the page are the supplier, invoice number, date, currency, lines and total: reading messy layout is understanding, which code cannot enumerate.
- Which rows are invoice lines (and not subtotal, tax, or footer rows): a reading judgment; a wrong pick is caught by the total check.
- Converting date formats, currency symbols and number formatting (`2 Oct 2026`, `€`, `1.234,50`) into ISO date, three-letter code and plain decimals: normalizing is reading. Not yet in code, which rejects such values with `InvoiceError` because the prompt does not ask for plain decimals and code only parses `Decimal(str(value))`.
- Supplier and description wording, as printed: transcribed, not matched to any ledger list; code only strips whitespace.
- Quantity and unit price when the invoice shows only a line amount: the model derives them; code then recomputes the amount.

## Constrained
- Empty text is refused before any model call: deterministic and free of cost.
- Extracting the JSON object from a fence or sentence, and failing with "not JSON" otherwise: output parsing is code's; the model's wrapping is untrusted.
- Required fields, their types and shapes (non-empty strings, valid ISO date, currency matching `[A-Z]{3}` after uppercasing, at least one line, numeric quantity/unit_price/total): downstream needs a fixed contract; unreadable input fails loudly rather than being guessed.
- Line amount = quantity × unit_price, rounded half-up to cents per line: arithmetic is exact and a policy, fixed in code.
- lines_total = sum of rounded line amounts; total rounded to cents: code computes, never takes the model's sum.
- Status is `ok` only on exact equality of lines_total and total, with no tolerance, else `mismatch`: the rule decides routing to a clerk and must be identical on every call.
- The model's total is never corrected to the lines (nor lines to the total): a mismatch goes to a human, not silently repaired.
- A missing description becomes an empty string rather than an error: lenient on purpose, since the amount does not depend on it.
- No retry, no repair loop: a failed or unreadable answer raises; a person decides what to do next.
- Negative or zero quantities, prices and totals (credit notes), and implausible dates, are accepted unchecked: nothing in code decides them; whether a credit note is allowed into the ledger is a policy for the owner and code should reject or flag it. Not yet in code, which accepts any finite number and any valid date.
- Currency is checked by shape only, so `XXX` passes: code should hold the list of valid ISO 4217 codes. Not yet in code, which checks only three capital letters.
- Invoices with tax, discount or shipping rows outside the lines: the total is "the amount due", and the lines may be net, so a VAT invoice reports `mismatch` (it goes to a clerk). Assumed.

## Target and budget
- Budget: exactly one model call per invoice; none for empty text; no retry.
- Target: every invoice either yields a fully typed record whose status was computed by code, or an error that names the field; nothing is guessed.
