I made the change the charter allows. It makes wrong lines less likely but cannot guarantee they never appear, and the guarantee you asked for needs a decision from you.

## What I changed
- **`seam.py`:** the prompt now tells the model that each reason is printed directly under the product's real price and rating, that customers will hold the shop to it, and that anything it says about price, rating or comparison with other products must be true of the listed figures.
- **`test.py`:** one new test checks that the prompt carries this instruction. All 14 tests pass.

This is guidance, not enforcement. The model can still write "under 100" for a 129.00 product, and the code will not catch it.

## The line I did not move
The charter for `recommend_products` lists the content of the reason as a free decision of the model, and says "claims in it are not checked." Making the reason reliably agree with the figures means code has to check or control it, which takes that decision away from the model. I'm not allowed to move that line, so I stopped here.

## Your options, if you want the guarantee
Each of these requires you to change the charter:
1. **Check and drop.** Code parses price, rating and ranking claims in the reason and blanks any reason that contradicts the catalogue. The product stays, and the charter already accepts an empty reason ("the right product without a reason beats no product"). Claim parsing is imperfect, so it would catch the Aria case but not every phrasing.
2. **Take numbers and comparisons out of the reason.** Code rejects or blanks any reason containing digits or ranking words such as "top-rated" or "cheapest". This is the most reliable option, but reasons get blander.
3. **Build those facts in code.** The model writes only the need-fit part of the reason, and code appends facts such as "Rated 4.6, the highest here" from the catalogue. This is exact, but it changes what the model writes.

Option 1 is the smallest change and keeps the model's wording. Option 2 gives the strongest guarantee against the "under 100" kind of complaint.