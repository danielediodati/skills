A partly unreadable invoice now comes back with everything that could be read, plus a list of what's missing. All 19 tests pass.

## What changed

- **Missing or unreadable fields:** each one comes back as `None` and is named in a new `missing` list.
  - Your two examples give `missing == ["invoice_number"]` and `missing == ["issue_date"]`, with supplier, date, currency, lines and total intact.
  - A bad currency code, absent lines or an unreadable total are handled the same way.
- **Lines:** a line with an unreadable quantity or unit price stays in the list, keeps its other values, and has `amount` of `None`. It is named as e.g. `"line 2 quantity"`. `lines_total` is `None` while any line amount is unknown.
- **Status:** an invoice with anything in `missing` gets `status: "incomplete"`, never `ok`, even if the lines happen to match the total. A clerk fills in only the listed fields.
- **Errors:** `InvoiceError` is still raised for empty text, an answer that isn't a JSON object, or when no field and no line value could be read.
- **Prompt:** I told the model to use `null` for anything it cannot read, so it doesn't guess.
  - That wording is my addition, not something you asked for.

## Charter

This moved a constrained decision. The charter said any bad field raises `InvoiceError`, so I updated the shape rule, the output description and the README in the same change.

The ledger rule is unchanged in intent: only `ok` goes in, and `mismatch` and `incomplete` go to a clerk.

## For downstream code

Any caller that treats "no exception" as "safe to book" must now check `status == "ok"`. The result dict also gains the `missing` key.

One shell command was denied by the sandbox, so I made the edits with the file tools instead. Nothing was left half-applied.