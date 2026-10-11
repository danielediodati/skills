A recommendation now never goes out with a reason that quotes a price different from the product's actual price. All 15 tests pass, including two new ones.

**What changed**
- In `seam.py`, after the reason is cleaned and capped at 80 characters, it is checked against the product's catalogue price. If it states a different price, the reason becomes `""` and the product stays in the strip.
- The check runs on the text the shopper would actually see.

**What counts as a price**
- A number next to a currency: `€14.90`, `$4`, `14,90 EUR`, `euros`, `dollars`.
- A number with exactly two decimals, such as `14.90`.
- A number right after a cue word (`at`, `only`, `just`, `for`, `costs`, `price`, `under`, `from`) with no word following it.

Quoting the right price passes (`19.90`, `€19,90`, `19.9`). Other numbers pass too (`2 m long`, `30-hour battery`, `Just 2 m of cable`).

**Limitations**
- It is a heuristic, not a full parse. A bare price with no currency, no decimals and no cue word (for example "a steal, 14") will slip through.
- A reason that mentions a different product's price correctly, such as "cheaper than the 7.50 one", will also be blanked. I chose to err on the safe side.

**Tests added in `test.py`**
- Your two examples (Pico earbuds at €14.90, the 2 m cable at $4) are blanked and the products kept.
- Correct prices and unrelated numbers are left alone.

**Decision for you:** if you would rather have a model-side fix too, the prompt could tell the model not to quote prices at all. I left the prompt untouched.