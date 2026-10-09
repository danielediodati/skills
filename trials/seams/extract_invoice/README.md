# extract_invoice

Used by an accounts-payable team to load supplier invoices into the ledger without retyping them.

`extract_invoice(text, model)` takes the plain text of one invoice (from a PDF or an email) and a model, any callable that takes a prompt string and returns a string. The model reads the invoice and reports the supplier, invoice number, issue date, currency, the invoice lines and the total.

The function returns a dict with `supplier`, `invoice_number`, `issue_date` (a `date`), `currency` (three capital letters), `lines` (each with `description`, `quantity`, `unit_price` and the computed `amount`), `lines_total`, `total` and `status`. Amounts are `Decimal`, rounded to cents. `status` is `ok` when the lines add up to the total and `mismatch` when they don't; a mismatched invoice goes to a clerk instead of the ledger.

If the model's answer can't be read, or a field is missing or malformed, the function raises `InvoiceError` with a message naming the field.

Run the tests with `python -m unittest` from this directory.
