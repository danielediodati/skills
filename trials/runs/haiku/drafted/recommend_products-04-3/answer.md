Nothing is changed yet. The fix needs a decision that the charter puts with you, so I stopped at that line.

**What I checked:** The 13 unit tests pass. Replaying your two examples with a stub model reproduces the bug: the reason text passes through unchanged ("Great sound for under 100" for the 129.00 Aria, "Our top-rated cable" for the 1 m cable rated 4.4 beside the 2 m at 4.6). The name, price and rating in each tile are correct. The fault is only in the reason line.

**The line:** `evals/recommend_products/charter.md`, under **Free**, says: "Wording of each reason: the model writes it for the customer, and code only collapses whitespace and cuts it to 80 characters." That is where the false claims come from. Your requirement, that reasons never state or imply a price, rating or standing that differs from the catalogue, can't be met while that line stays free. Moving it to Constrained is your call, and I can't edit the charter myself.

**What moving it would buy, depending on the option you pick:**
- **Drop reasons (simplest):** the model still picks and orders the products, but the strip shows no reason line. This guarantees agreement, and it loses the "why it suits" text.
- **Fixed templates from catalogue data:** the reason is built from the product's own facts, such as "Rated 4.6 from 2 m cable". This guarantees agreement but is less personal.
- **Code check on model text:** reject any reason containing a figure, currency amount or comparison word ("top", "best", "cheapest", "under"). This keeps the model's wording but is blunt and will drop some good reasons. It also can't reliably catch "top-rated" claims, which need comparing against other products.
- **Prompt rule only** ("don't mention prices, ratings or rankings"): I would not rely on this alone. It is not a guarantee, and it may itself count as a line move under the charter.

**My recommendation:** given the consumer-protection exposure, go with dropping reasons or fixed templates. The check-based option leaves gaps you would have to explain to customers again.

Tell me which option you want, and I'll get the charter updated by you, then make the change and add tests. No paid calls were made.