A reason that contradicts the price or rating shown for its product is now replaced with an empty reason, so it can't appear under the wrong figures. All 17 tests pass (13 existing, 4 new).

**What changed (`seam.py`)**
- **Prompt:** it now tells the model that the reason is printed beside the listed price and rating and must agree with them. This is a criterion for the model, not a script for it.
- **Check after the picks are built:** each reason is compared with the catalogue figures, and a reason that fails is blanked. Which products appear, their order and their wording are still the model's.
  - **Figures:** every number in the reason must be the product's price or rating, or sit behind a bound that is true for it ("under 150" is kept for 129.00, "under 100" is not).
  - **Standing:** "top-rated", "cheapest" and similar claims must hold against the other products in the strip. Comparatives such as "cheaper" or "better rated" are always blanked, since they can't be verified.

Both of your cases now come out with an empty reason: the Aria with "under 100", and the 1 m cable with "Our top-rated cable" next to the 4.6-rated 2 m cable.

**Limits**
- The check is number and keyword matching, not an understanding of the sentence. A contradiction worded in some other way, such as "a bargain" or "the best value of the lot", would still get through. Only a model judge, or a fixed template for reasons, would catch more.
- It is deliberately conservative. A true but unrelated number, like "1 m" in the cable's reason, is blanked too.
- A claim of "top-rated" is compared against the products in the strip, as in your example, not the whole catalogue.

**Your decision:** if you want reasons that never state a figure or comparison at all, a fixed template would guarantee it. That would take the reason away from the model, so I left it for you to decide.

I also documented the behaviour in `README.md` and added the four tests to `test.py`.