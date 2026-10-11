A reason that quotes a price different from the product's own is now emptied, and the product stays in the strip. All 17 tests pass, including four new ones for this.

**Code (`seam.py`)**
- After the reason is cut to 80 characters, `states_other_price` looks for prices in it and compares each with the catalogue price.
- It treats a figure as a price when a currency sits next to it (`€14.90`, `$4`, `19,90 EUR`, `4 euros`) or when it is written with two decimals (`19.90`).
- Other numbers such as "2 m long", "30-hour battery" or "Rated 4.5" are left alone, and a correct price like "Solid choice at 19.90" is kept.
- Thousands separators are handled, so `€1,299.00` matches 1299.0.

**Charter (`evals/recommend_products/charter.md`)**
- The charter listed "claims in the reason are not checked" as free, so this moves a decision from the model to code.
- I updated the charter in the same change: price is now a constrained claim, and the rest of the reason stays free.

**Limitations**
- A bare whole number with no currency ("only 15") is not recognised as a price, because it can't be told apart from "15 hours" without more context.
- A reason that uses an unusual currency word the pattern doesn't cover would slip through.
- Say if you want either case tightened. The usual cost is more good reasons being blanked.