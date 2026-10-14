The reason line can no longer state a price, rating or ranking that the shop doesn't show. Both of your examples are now caught: "Under 100, great sound" and "Our top-rated cable" come back with an empty reason, and the card still shows the real price and rating. All 17 tests pass with `python -m unittest`.

**What changed in `seam.py`**
- **Prompt:** the model is told not to mention any price, rating, or how a product ranks or compares with the others.
- **Filter:** after the model answers, any reason containing a digit, a currency sign, or a price, rating or ranking word is blanked. The list covers words like under, cheap, price, value, rated, stars, review, top, best, cheapest, better and popular.
- **Order:** the reason is cleaned and checked before it is cut to 80 characters.

**What changed in `test.py`**
- Several existing tests used "Best sound" or "Light and cheap" as sample reasons. The new filter would blank them, so I changed the wording in those tests to claim-free text.
- New tests cover the Aria "under 100" case, the "top-rated" cable case, a set of comparison phrases, and the prompt wording.

**What changed in `README.md`**
- It now says that a reason making a price, rating or standing claim is returned empty.

**Choices I made that you may want to change**
- I blanked the reason rather than dropping the product. A product still shows up with its real figures and no reason line.
- The filter is a word list. It fails safe, since anything it catches is blanked, but a claim phrased in a way it doesn't list could still get through. The prompt change is there to reduce that. If you see one slip through, send me the text and I'll add it.
- The list is fairly broad. It also blanks harmless words such as "value" or "first", so some good reasons will now be empty. That is the trade-off for keeping every price and ranking claim out.