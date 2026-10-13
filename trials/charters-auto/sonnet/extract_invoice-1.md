# extract_invoice charter

Input: the plain text of one supplier invoice (from a PDF or an email), and a model callable (prompt string in, string out).
Output: a dict with `supplier`, `invoice_number`, `issue_date` (`date`), `currency` (3 capitals), `lines` (`description`, `quantity`, `unit_price`, computed `amount`), `lines_total`, `total` (all `Decimal`, cents) and `status` (`ok` or `mismatch`); or an `InvoiceError` naming the field.

## Free
- Reading the invoice: which text is the supplier, invoice number, issue date, currency, each line and the amount due, in whatever layout, language or wording the document uses. Layouts are unbounded and nobody can write rules for them; this is the whole reason the model is here.
- Which lines count as invoice lines (items, delivery, discounts, tax rows) and how each is split into description, quantity and unit price. The invoice's structure varies and the code has no rule for it.
- Normalising the date to YYYY-MM-DD and the currency to a code (symbol or word to code) from how the invoice writes them. It is a reading judgement; code only checks the result.
- The wording of descriptions and of the supplier name, kept as the invoice has them (code only trims whitespace).
- Which figure is "the total amount due" as printed on the invoice. The model reports it; code never derives it from the lines.

## Constrained
- Number of model calls: exactly one per invoice, no retry, no second opinion, no repair prompt. A bad answer is an error for a person to handle, not a loop; this keeps cost and latency fixed.
- Empty or blank text is refused with `InvoiceError` before the model is called, so no call is spent on nothing.
- Answer format: a single JSON object with fixed keys, requested by the prompt ("JSON object only"). Code takes the span from the first `{` to the last `}` to tolerate fences and chatter; anything not parsing to an object is `InvoiceError`. Format drift must not become silent data.
- Required fields: supplier, invoice_number, issue_date and currency must be non-empty strings, and there must be at least one line. Missing means error; code never guesses or fills a default, because a wrong ledger entry is worse than a rejected one.
- Date: must be a valid ISO date or `InvoiceError`. Code does not repair free-form dates ("2nd October"); the model owns the conversion, code owns the check.
- Currency: upper-cased, then must be exactly three letters A-Z. The check is on shape only; it is not checked against a list of real ISO codes (today's looseness, not a stated decision).
- Numbers: quantity, unit_price and total must be finite decimals (bool, missing and NaN/Infinity are rejected). Parsed as `Decimal` from the string form, never float, so cents are exact. A missing or unreadable number is an error and is never defaulted to 0 or 1.
- Line amount: computed in code as quantity × unit_price, rounded half-up to cents. The model's own line amounts are never asked for or used, so arithmetic cannot be hallucinated.
- Total: rounded half-up to cents; `lines_total` is the sum of the rounded line amounts, computed in code.
- Status: `ok` only when `lines_total == total` exactly (no tolerance), otherwise `mismatch`. A mismatch is a result, not an error: it is returned with all fields so a clerk can review it, and code never corrects the total or a line to force agreement. The rule decides what reaches the ledger, so it stays deterministic and auditable.
- Description: never required; missing becomes an empty string, trimmed.
- Error handling: every failure is an `InvoiceError` with a message naming the field (`supplier is missing`, `line 1 quantity is missing`, ...). Callers and tests rely on these messages and on this single exception type.
- Output types and shape: fixed keys, `date` and `Decimal` types, line order as the model returned it. Downstream ledger loading depends on them.
- Model interface: a plain callable taking a prompt string; the prompt text is fixed in code and embeds the invoice text unchanged.

## Budget
- Budget: one model call per invoice; no timeout, token limit or retry is set in this seam. The single call is a design choice (errors surface to a clerk), not a tuned number. Cent precision (0.01, half-up) and the zero tolerance on `status` are business rules, not budgets.
