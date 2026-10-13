An ambiguous issue date is now refused with an error instead of being loaded as if it were certain. I haven't run it against a real model, so I can't yet say whether Brightwell BP-2304 comes out as 5 August 2026. The 18 local tests pass; they use a fake model and no paid calls.

**What changed**
- **Prompt (`seam.py`):** for a date written only in numbers, the model is told to settle day-first or month-first from the evidence on the invoice. That evidence is the supplier's country and address, the currency, a day above 12 in this or another date, month names, and the payment-terms wording. It also reports a new `issue_date_ambiguous` true/false value, set to true if the date can still be read two ways after weighing that evidence.
- **Code (`seam.py`):** `issue_date_ambiguous: true` raises `InvoiceError("issue_date is ambiguous: ...")`. A missing or non-boolean flag raises `InvoiceError` naming that field, so a date can't slip through unmarked.
- **Tests (`test.py`):** added cases for the ambiguous flag, the missing flag, a resolved day-first date, and the prompt carrying the evidence.

**What stays with the model, and what code decides**
- **Model:** reading which day or month comes first remains the model's call. I added no rule such as "GBP means day-first".
- **Code:** only the ambiguity refusal is in code. The output shape and the `ok`/`mismatch` status are untouched, and I didn't edit the charter.

**What to expect**
- **Brightwell:** a British supplier with a day-first date should now resolve to 5 August 2026.
- **The US case:** an American supplier's "03/04/2026" with no other evidence will be refused rather than loaded, so a clerk has to enter it. That is the intended trade-off.
- **Risk:** the model can still be confidently wrong and report "not ambiguous". The flag lowers that risk but cannot remove it.

**Decision for you**
Refused invoices raise an error rather than going to a clerk with a flagged date. Carrying a "date unconfirmed" marker through to the clerk would need a new output key or status, which changes the shape the ledger loader depends on. That is your call.

**Next step**
If you want it, I'd check the prompt on real invoices, including BP-2304 and the American "03/04/2026" one. That spends money, so I need your approval and a budget before the first call. A small run of about 10 calls on the cheapest model first seems enough; tell me the number you're comfortable with.