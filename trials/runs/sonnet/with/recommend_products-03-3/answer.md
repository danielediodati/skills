I haven't changed anything yet, because this fix moves a line the charter draws, and `AGENTS.md` says that decision goes to you first.

**The conflict.** `evals/recommend_products/charter.md` lists the reason's content as free to the model, and it says so explicitly: "What each reason says: a good one says how the product meets the need; claims in it are not checked." It also lists "Name, price and rating come from the catalogue, never from the model" as constrained. Your bug sits where those two meet: the price field is safe, but a price written inside the free-text reason is not.

**What I'd propose.** I'd narrow the "not checked" rule rather than drop it:

- In `seam.py`, after the reason is cut to 80 characters, find the price-like numbers in it: a number with a currency symbol or code (`€14.90`, `$4`, `14.90 EUR`), or a decimal such as `19.90`.
- If any of those figures differ from the product's catalogue price, set the reason to `""`. The product stays in the strip, and the charter already says an empty reason is kept.
- Leave other numbers alone ("2 m long", "30-hour battery"), and keep a reason that quotes the correct price ("Solid choice at 19.90").
- Keep it to one model call with no retry, and don't change the prompt.

**Charter change, in the same commit.**

- **Free:** reason content is still the model's, but a stated price must match the catalogue.
- **Constrained:** add "a reason that states a price other than the product's is blanked, and the product stays".

**Limits.**

- Without a currency symbol, a bare integer is ambiguous ("2 m", "30-hour"). I'd only treat bare numbers as prices when they have a decimal part or a currency marker. A reason like "only 15 bucks" would slip through.
- Comparative claims ("half the price of the 2 m version") aren't caught unless they contain a figure. Your cable example is caught only because it says "$4".

Shall I go ahead with this, and update the charter and add tests in the same change? Tell me if you'd rather block more aggressively, for example any number next to a currency word.