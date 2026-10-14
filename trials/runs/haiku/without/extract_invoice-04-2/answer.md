Invoices with European amounts now load. The Kessler total comes through as 1250.00, and the Cartiera unit price as 2340.50. All 20 tests pass, including 6 new ones.

There were two changes, both in `seam.py`:

- **Prompt:** the model is now asked to write every amount as a plain number with a dot as the decimal point and no thousands separators. So "1.250,00" should come back as 1250.00 before it reaches the parser. This is the main fix, since the model can see the whole invoice.
- **Number parsing:** `_number` now reads both styles. When both separators appear, the one written last is the decimal point, so "1.250,00" and "1,250.00" both work. "1.250.000" reads as one million two hundred and fifty thousand.

I made one judgment call you should know about. A comma followed by exactly three digits, such as "1,250", could mean one thousand two hundred and fifty or one and a quarter. The function raises `InvoiceError: ... is ambiguous` rather than guessing. That invoice still gets refused, so a clerk has to key it in. I think a wrong amount is worse than a refusal here, but say if you want the other reading.

Limits to be aware of:

- A dot followed by three digits, such as a bare "1.250" from a German supplier, still reads as 1.25. The existing test expects "0.335" to be decimal, and I left that behavior alone. The prompt change is what protects these cases.
- I could not test the prompt change against a live model. The tests use a fake model, so please run a few real invoices from the continental suppliers before relying on it.
- Amounts with a currency symbol or code attached, such as "€1.250,00", are still refused.