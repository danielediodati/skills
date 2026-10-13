A reason that misstates the price, rating or standing shown beside it is now dropped, and the product stays in the strip. All 18 tests pass, including 5 new ones.

**What changed**

- **`seam.py`, prompt:** it now tells the model that price and rating are displayed next to its reason, and that the reason must not state or imply figures or rankings that differ from the list.
- **`seam.py`, new check in code:** after the picks are chosen, each reason is checked against the figures the shop shows for that product. A reason that contradicts them is replaced by an empty reason, which the function already allowed. The checks cover:
  - **Price limits:** "under 100", "over 50" and similar, compared with the product's price.
  - **Quoted amounts:** "$99", "50 EUR" and similar must match the price to within 1.
  - **Quoted ratings:** "rated 4.9", "4.7 stars" and "4/5" must match the rating.
  - **Standing:** "top-rated" and "cheapest" (and "most expensive") must hold among the products in the strip.
- **`test.py`:** tests for wrong and true prices, wrong and true ratings, and the top-rated and cheapest comparisons within the strip.

**Your two examples**

- The Aria at 129.00 with "Great sound for under 100" now shows no reason.
- The 1 m cable rated 4.4 with "Our top-rated cable", next to the 2 m cable at 4.6, now shows no reason.

**What I left alone**

Which products are picked, and their order, is still entirely the model's decision. The check only stops a false line from being displayed.

**Limits**

- The check recognises the common phrasings above, not every possible way of stating a price or rating. A reason like "a steal at half the price of rivals" would pass.
- "Top-rated" and "cheapest" are judged against the products in the strip, which matches your cable example. If you want them judged against everything in stock in the catalogue, that is a one-line change; you would need to say which you mean.
- If you would rather never show free-text reasons that contain figures or comparisons at all, that is a stricter rule I did not apply, because it would also remove true statements. Say if you want it.