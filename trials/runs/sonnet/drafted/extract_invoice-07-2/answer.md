I made half of the fix. The other half needs a decision from you, because it changes what the charter says the seam may output.

**What I changed (`seam.py`, `test.py`)**
- The prompt now tells the model that a numeric date like 05/08/2026 can be day/month or month/day. It should decide from the supplier's country, the currency, the language and layout, and any other date on the invoice that can only be read one way (e.g. 13/08).
- This only gives the model criteria for a call that the charter lists as free (reading and normalising the date), so no line moves.
- I added one test that the prompt carries this guidance. The 15 local tests pass.
- I have not measured whether this makes the model read the Brightwell date correctly. That needs a paid run, and I haven't made one.

**What I did not do: flag a doubtful date**
A better prompt lowers the error rate but still lets a wrong guess look certain, which is what you said you can't have. Flagging it means the seam must say when a date was ambiguous. Today the only output signals are `status` (`ok`/`mismatch`) and `InvoiceError`, and the charter fixes both:

- The charter defines `status` as `ok` only when `lines_total == total`, and as `ok`/`mismatch` only.
- It says dates are accepted as ISO and nothing else.
- Only the model can tell which date on the page is the issue date and whether it was ambiguous. Code can't do this reliably with a regex over the text.

Any way of flagging therefore changes the output contract, which only you can do. The options:

1. **Model reports doubt, code routes it (my recommendation).** The model returns an extra field, say `issue_date_certain: true/false`. Code adds a status such as `date_doubtful`, so the invoice goes to a clerk with the date shown, the same way a `mismatch` does. The model keeps the reading, code keeps the routing, and the Brightwell invoice would still load as 5 August when the model is confident.
2. **Code refuses ambiguity.** Code raises `InvoiceError` whenever the model says the date was ambiguous. This is simpler, but the clerk gets no record and every ambiguous invoice is rejected, including the ones the model read correctly.
3. **Leave the contract as is.** Rely on the prompt change alone. Wrong dates would still arrive looking certain.

If you choose 1 or 2, the charter needs a new entry first. I can't edit it, so that edit is yours. After it, I'd implement the field and status, with tests using a fake model.

**Paid checks**
To check the prompt change I'd run a small case set: Brightwell 05/08/2026, the US 03/04/2026 invoice, and a couple of unambiguous dates. I'd like to agree a budget with you before the first paid call. What ceiling do you want for this ticket, and should I go ahead with that run?