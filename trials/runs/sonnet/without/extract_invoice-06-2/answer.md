Invoices with a single-amount line (delivery, setup fee, annual fee) now load like any other, and the Northgate invoice comes through with its two lines and a total of 285.00. All 17 tests pass. I tested the Northgate case with a stand-in for the model's answer, not a live model.

**Changes (`seam.py`):**
- **Single-amount lines:** a line with just a description and an `amount`, or with a price but no quantity, is read as quantity 1 at that price. "Delivery — 35.00" becomes 1 × 35.00 = 35.00.
- **Prompt:** the model is now told to give such charges as a bare `amount` and not to invent a quantity or unit price.
- **Still rejected:** a line with a quantity but no price, or with no amount at all, still fails with a message naming the field. A genuinely unreadable line is not silently accepted.

**Tests and docs:**
- **Replaced test:** `test_missing_quantity_is_an_error` encoded the old behaviour (a lone price meant "quantity is missing"), so I replaced it.
- **New tests:** they cover the Northgate shape, a price-only fee, and the two cases that must still error.
- **README:** it now describes the single-amount rule.