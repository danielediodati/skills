Reasons that state a price or rating are now dropped before they reach the page, so the Aria and the "top-rated" cable would both show with no reason. The unit tests pass (18 of 18, up from 13). I haven't tried the change against the real model.

**Why it happened:** `seam.py` passed the model's reason straight through. The prompt never told the model to keep prices and ratings out of it, and nothing checked the text against the catalogue.

**What changed:**
- **`seam.py`**: the prompt now tells the model not to mention prices, ratings, numbers, discounts, or rankings on price or rating. After the reply comes back, any reason that still has digits, a currency symbol, or words like "under", "cheaper", "cheapest", "top-rated", "best value", "budget", or "5-star" is blanked. The product stays in the strip without a reason. The code already allowed an empty reason.
- **`test.py`**: added tests for both reported cases, several phrasings of price and rating claims, a check that ordinary reasons like "Over-ear comfort and clear sound" still pass, and a check that the prompt carries the new instruction. The existing "Light and cheap" test case became "Light and compact", since "cheap" is a price claim and would now be blanked.
- **`README.md`**: documents the rule.

**Limits:**
- This is a word filter, so it can miss a paraphrase it doesn't list, such as "a bargain" or "pricey". Those are only partly covered by the list in `PRICE_OR_RATING_CLAIM`.
- Quality claims like "Best sound" are still allowed. The catalogue has no sound data to check them against, so I left them alone.
- If you want a guarantee rather than a filter, the stronger fix is to stop writing free-text reasons about price or rating at all and build those lines from the catalogue fields.

Two things I didn't do: this folder isn't a git repository, so there's no commit, and I didn't run the prompt change against the model. A quick check with a few real searches would show whether the model's reasons are now mostly kept or mostly blanked.