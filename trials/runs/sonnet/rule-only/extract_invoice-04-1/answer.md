Amounts written the continental way now load. The Kessler total `1.250,00` comes through as `1250.00`, and the Cartiera Lombarda unit price `2.340,50` as `2340.50`. All 17 tests pass, including the new ones.

**The change:** `_number` in `seam.py` now rewrites printed amounts into plain decimals before parsing them, via a new `_plain_decimal` helper. The prompt and the model's job are untouched. The model still reports amounts as printed, and the code decides how to read them.

**Notations now read:**
- `1.250,00` → 1250.00
- `1,250.00` → 1250.00
- `1 250,00` (space or non-breaking space) → 1250.00
- `12,5` → 12.5
- `1.250.000` and `1,250,000` → 1250000

**Still refused:** a lone comma followed by exactly three digits, such as `1,250`, is refused with the existing "is not a number" error. It could mean 1,250 or 1.250, and a wrong guess would put a thousandfold error in the ledger. Malformed groupings like `1.2.3` are refused too.

**Your call:** `1.250` with a single dot and no comma is still read as 1.250, as before, because a three-decimal price such as `0.335` is already in the tests. A German invoice that prints a bare `1.250` meaning one thousand two hundred and fifty would therefore load as 1.25. If you want that case refused as ambiguous, or read using the invoice currency or supplier country, that is a decision for you to make.

I added tests for continental amounts, the notation table and the ambiguous cases in `test.py`.