# extract_invoice charter

Input: the plain text of one supplier invoice, and a model
Output: supplier, invoice number, issue date, currency, lines with computed amounts, lines total, total and a status (`ok` goes to the ledger, `mismatch` to a clerk); or `InvoiceError`

## Free
- Which text is the supplier, the invoice number, each line's description: reading invoices laid out by every supplier differently is why the model is here.
- What an ambiguous date means (`02/10/2026`): the model sees the supplier's country and language; a fixed day-month rule would be wrong for half of them.
- Which currency the invoice is in (`€`, `EUR`, or nothing stated): inferring it is reading.
- Which entries are lines (delivery, discounts): the layout differs per supplier.
- Negative amounts, for discounts and credit notes: they are real invoice content.
- Non-integer quantities (hours, metres, kilos): a whole-number rule would be no real constraint.
- An empty line description: it serves the clerk, not the check.
- The supplier's name, as written: there is no supplier registry to match against; with one, membership would be a constraint.

## Constrained
- The answer's shape: one JSON object with the named keys, `issue_date` as `YYYY-MM-DD`, at least one line; anything else raises `InvoiceError` naming the field. A record that cannot be checked must not reach the ledger.
- Currency in ISO 4217: the list of valid codes is closed and complete. Not yet in code, which only checks three capital letters.
- Net, VAT and total as separate fields, with the arithmetic between them checked by code. Not yet in code: today the total is the amount due, so a VAT invoice whose VAT is not reported as a line comes out `mismatch`.
- Line amounts computed by code (quantity × unit price, rounded half-up to cents), never read from the model: arithmetic has an answer written before anything runs.
- The lines must add up to the total to the cent, no tolerance; otherwise `mismatch` and a clerk. A wrong record in the ledger costs more than one checked by hand.
- One model call, no retry, no fallback: the cost per invoice is fixed, and an error already sends the invoice to a person.
- The mechanical steps: empty text refused before the model is called, JSON read from inside a code fence or a sentence, currency upper-cased.

## Target and budget
- Budget: one model call per invoice.
