The strip can't yet guarantee that nothing outside the price limit is shown. Making that guarantee means moving a line in the charter, and that decision is yours.

**What I changed**
- `seam.py`: the prompt now tells the model that when the search states a price limit or range (`under 50`, `max 30 euro`, `from 100`, `between 20 and 40`), it should only pick products within it. The model already sees every price, so this is criteria for its judgement.
- `test.py`: one test checks the instruction reaches the prompt. All 14 tests pass.

**Why this isn't a guarantee**
A hard "nothing outside the limit" guarantee needs code to parse the price out of the query and drop products that fall outside it. The `recommend_products` charter (`evals/recommend_products/charter.md`) doesn't allow that in either place:
- **Filtering before the call** is explicitly constrained: the model sees every in-stock product, and code does not narrow the catalogue.
- **Filtering the picks afterwards** takes over part of "which products suit the search", which the charter lists as free for the model.

Either way a code rule would decide suitability instead of the model. Today the model can still occasionally ignore the instruction and return a 129.00 pair of headphones for `under 50`.

**Your options**
1. **Keep the prompt-only change.** It is probably much better than before, but there is no guarantee.
2. **Change the charter** to make price limits a constrained rule. I would add a post-call filter: parse the limit from the query, drop out-of-range picks, and return an empty strip if none remain. This keeps the model seeing the full catalogue and keeps one call. It delivers exactly what you asked for, including the empty strip. If you edit the charter, I'll implement it.