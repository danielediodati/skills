I made a partial fix. The part that guarantees the reason never contradicts the figures needs a decision from you, because it moves a line in the charter.

**What I changed**
- `seam.py`: the prompt now tells the model that the customer sees each product's price and rating beside its reason. It also says that anything the reason states about price, rating or comparison with the other products must match the list.
- `test.py`: one test checks that this instruction reaches the model. All 14 tests pass.

**Why this isn't a guarantee**
This only makes the model more likely to get it right. Nothing in code checks the reason, so an "under 100" line on a 129.00 product can still appear. The charter lists the wording of reasons as a free decision and says nothing checks it against the catalogue. That is exactly the gap behind your two examples.

**The line to move**
Enforcing "the Aria never appears with a reason that promises a price it doesn't have" means code takes over part of the reason. There are three ways to do it:

1. **Check and blank (my recommendation).** Code scans each reason for price, rating and ranking claims, such as numbers, "under N", "top-rated" and "cheapest". If a claim disagrees with the catalogue, or can't be verified, the reason is replaced with an empty one. The pick stays, as the charter already allows reasons to be empty. This is a guarantee with the least loss, but a rule-based scan will miss some phrasings. You'd need to decide how strict it should be, for example blanking any reason that contains a digit or a superlative.
2. **Ban such claims.** Code or prompt forbids figures and comparisons in reasons altogether. This is easy to verify, but reasons lose useful content.
3. **Generate the claims in code.** Code fills in the price and rating phrases from the catalogue, and the model writes only the non-factual part. This is the most reliable, but it takes the most wording away from the model.

Each of these narrows what the charter calls free, so I haven't done any of them and haven't touched the charter. Tell me which you want and update the charter yourself. I'll then implement it and add tests using your two examples.