I made the part of the fix I can, but it can't give you the guarantee you asked for without a decision from you.

**What I changed**

In `seam.py`, the prompt now tells the model that the price and rating are shown next to its reason. It must not state a price or rating the product doesn't have. It must not call a product cheapest, top-rated or best value unless the list shows that. If it can't say something true about the figures, it should say how the product meets the need instead. The model already sees every in-stock product with its price and rating, so it has what it needs to compare.

This should make the "under 100" and "top-rated" lines much rarer. It is still a request to the model, so it doesn't make them impossible, and I haven't run it against a real model.

**The line I didn't move**

The charter for `recommend_products` lists "what each reason says" as a free decision, and states that "claims in it are not checked". A real guarantee that the Aria never appears with an "under 100" reason needs the code to check the reason against the catalogue. That is, parse prices, ratings and "top-rated" or "cheapest" claims out of the reason and drop or replace any reason that contradicts the shop's figures. That would move the line from free to constrained, so I haven't done it and I haven't touched the charter.

**What moving the line would buy**

Contradicting reasons would be stopped in code rather than discouraged in the prompt. Two things come with that:
- Detection of comparative claims in free text ("our top-rated cable") is imperfect, so the check would be strong on numbers and weaker on wording.
- The charter would also have to say what happens to a rejected reason. The current charter keeps an empty reason ("the right product without a reason beats no product"), so blanking the reason would fit that.

If you want that check, tell me and update the charter to say so. I can then build it.