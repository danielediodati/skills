A reason that quotes a price different from the product's catalogue price is now blanked, and the product stays in the strip. All 15 tests pass, including two new ones for this.

**What the check does** (`seam.py`)
- **Wrong price:** both of your examples ("only €14.90" under 19.90, "just $4" under 9.50) come out with an empty reason. The product itself is kept.
- **Correct price:** "Solid choice at 19.90" and "€19.90" stay.
- **Other numbers:** "2 m long" and "30-hour battery" stay.
- **What counts as a price:** a number next to a currency symbol or word (€, $, £, EUR, euro(s), dollar(s)…), or a number with two decimals such as `14.90` or `14,90`.
- **What the check sees:** it runs on the reason after the 80-character cut, so a price cut in half by the truncation is also blanked.

**Limit:** a bare whole number with no currency mark, like "for 15", isn't recognised as a price and passes. Catching it would also flag "2 m" and "30-hour", so I left it out.

**Charter change you should confirm**
- The charter listed "claims in it are not checked" as free, so this moves a line.
- I treated your request as that decision and updated `evals/recommend_products/charter.md` in the same change.
- "Claims are not checked" now carries an exception for price, and Constrained has a new entry stating the rule.
- The charter's existing principle that the right product without a reason beats no product is what keeps the product in the strip.

There's no git repository here, so nothing is committed.