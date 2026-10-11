I made only part of the fix. The prompt now tells the model to keep reasons consistent with the figures, but nothing in code checks them, so the Aria could still appear with "under 100".

**What I changed**

In `seam.py`, the prompt now tells the model that the price and rating are shown next to its reason. Any mention of price, rating or comparison must match the listed figures. If it isn't sure a claim holds, it should say how the product meets the need instead. The existing 13 tests pass.

This lowers how often the problem happens. It does not guarantee the Aria never shows "under 100".

**The line I can't move**

The charter at `evals/recommend_products/charter.md` lists the content of the reason as a free decision for the model: "What each reason says: … claims in it are not checked." Guaranteeing what you asked for means code checking claims, and that moves this line. Only you can change the charter.

**What moving it would buy**

- **Code-side check:** when a reason states a price, rating or ranking that contradicts the catalogue, the code would blank the reason or drop the pick. Wrong claims could no longer reach the strip.
- **Cost:** a pick with a wrong claim loses its reason. Checking free text for numbers and phrases like "top-rated" is also imperfect.
- **Alternative:** the code could ask the model to write reasons that make no price, rating or comparison claims at all. Reasons would be safe by construction but less informative.

Tell me which you prefer and update the charter, and I'll implement it. Until then, the prompt change is the extent of what I can do.