I haven't changed anything. Fixing this as asked would move a line in the charter, and only you can decide that.

**Why it happens.** The model writes each reason after seeing the whole catalogue, so it can say "under 100" or "top-rated" without checking them against the product's own figures. The code deliberately takes price, rating and name from the catalogue, but it doesn't look at what the reason says.

**Where the line is.** `evals/recommend_products/charter.md` lists "the wording and content of each reason" as free: "code only checks its length and shape". It also says there is no validation of the reason's truthfulness, though it marks that as today's behaviour rather than a rule. A guarantee that the Aria never shows "under 100" has to be enforced in code, which takes part of that decision away from the model. It also touches the "prompt shape is fixed" line.

**Options**

1. **Prompt criterion only.** Add a sentence telling the model not to state or imply a price, rating or ranking that the listed figures don't support. This informs the model's judgement and doesn't move the free line, but the charter lists the instruction wording as fixed. It reduces the problem but does not guarantee it.
2. **Code check on the reason.** Code inspects each reason and blanks it (the charter already allows `""`) or drops the pick when it contains figures or comparative claims. This is a guarantee only for digits and currency. Phrases like "top-rated", "cheapest" or "under a hundred" can't be reliably detected by pattern matching.
3. **Code-written facts, model-written reason.** Code prints the price and rating, and the reason is restricted to a closed set of claims code can verify, or has no comparative claims at all. This is the only complete guarantee, but it removes most of the model's freedom over reason wording.
4. **A model judge that checks each reason against its product's figures.** It is a new seam with its own charter, it costs a paid call per request, and it is still not a hard guarantee.

**Recommendation:** option 2 plus option 1. Blank reasons that contain digits or currency symbols, and tell the model in the prompt not to make price, rating or ranking claims. That catches "under 100" outright and makes "top-rated" rarer. If "top-rated" must also be impossible, only option 3 does it.

Which would you like, and do you approve the charter change it needs? The charter is yours to edit, and I won't touch it. Once you decide, I'll write the code and tests. The tests are free and local; I won't run anything paid without agreeing a budget with you first.