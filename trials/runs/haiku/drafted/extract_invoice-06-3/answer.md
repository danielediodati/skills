I did not change the code. The fix you want moves a line in this seam's charter, so AGENTS.md says to stop there and leave the decision to you.

**What I reproduced**

The 14 existing tests pass. The Northgate answer with no `quantity` on the delivery line is refused with `InvoiceError: line 2 quantity is missing`, which matches what you saw.

**Where the line is**

`evals/extract_invoice/charter.md` puts these under **Constrained**:

- **Prompt text** (line 16): a fixed template, "Tightness: exact." Adding a hint such as "a single-amount charge has quantity 1" would change that template.
- **Required fields** (line 19): "Missing means error, not a guess."
- **Each line** (line 22): numeric `quantity` and `unit_price` are required, "Tight on type."

The charter's **Free** section already gives the model the derivation: "Deriving quantity and unit price when the invoice gives only a line amount" (line 12). In the Northgate case the model did not supply quantity 1 for the delivery line, and nothing in code can make it do so without touching a constrained line.

**Options, each of which moves a line**

1. **Default a missing quantity to 1 in `_number` / the line loop.** Loosens the type check and turns a missing field into a guess, which line 19 forbids.
2. **Add a rule to `PROMPT`** so the model fills quantity 1 for single-amount charges. Changes the fixed prompt template, which line 16 forbids. This is the option that keeps the model doing the derivation, as the Free section intends.
3. **Allow `quantity` to be null on a line** and skip the amount for it. Loosens the type check, and `lines_total` would then need a rule for that case.

**What it would buy**

With quantity 1 and unit price 35.00 on the delivery line, the Northgate invoice would load with the two lines, a delivery amount of 35.00, `lines_total` 285.00 and `status` `ok`. The same would hold for the IT support fee and the printer's setup charge.

**What I need from you**

Tell me which option to take, or edit the charter yourself to permit it. I will not edit the charter. Once the line has moved, I can make the code change and add tests for the Northgate case. No paid model calls were made, and none are needed for that work.