I made only the part of this change that the charter allows, so the price limit is not yet guaranteed. Tests pass (14).

**What I changed**
- `seam.py`: the prompt now tells the model that if the search states a price limit or range (`under 50`, `max 30 euro`, `from 100`, `between 20 and 40`), it should pick only products within it, and pick none if nothing is.
- `test.py`: a test that the prompt carries that instruction and the shopper's price text.

The model already sees every price, and an empty answer already gives an empty strip, so this should cut most of the out-of-range picks. Nothing in code enforces it, though. The model can still ignore the limit.

**The line I stopped at**
To guarantee that nothing outside the limit appears, code would have to parse the price out of the search and drop picks outside it (or hide those products from the model before the call). The `recommend_products` charter puts both on the model's side:
- *Which products suit the search* is free for the model to decide. A code filter on price would take part of that decision.
- Narrowing the catalogue before the call is explicitly constrained, which rules out the "hide them from the model" route.

A regex also can't tell `cable max 2 m` or `under 50 pieces` from a price, which the model reads correctly.

**What moving it would buy**
Moving the line would make the limit a hard guarantee. It would cost the model's reading of ambiguous phrasing, and shoppers could get an empty strip where the regex misreads something that wasn't a price. If you want that, the smallest version is a post-filter on the model's picks using a parsed price bound, and the charter would need to list "price bound stated in the search" as constrained. That decision and the charter edit are yours.