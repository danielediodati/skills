Reasons that state a price, a rating, or a ranking are now dropped before they reach the shopper. The product stays in the strip with a blank reason, which the existing contract already allows. All 16 tests pass.

The cause was that `recommend_products` passed the model's reason text straight through. I made two changes in `seam.py`:

- **Prompt:** the model is now told not to mention prices, ratings, or how a product ranks against the others.
- **Code check:** every reason is checked after generation. It is cleared if it contains a digit or currency sign, or any of these words: price, cost, under/below/over/above, cheaper/cheapest, deal, discount, sale, offer, value, top, highest/lowest, most/least, more/less, popular, favourite, bestseller/best-selling, rated/rating, stars, reviews.

The prompt is a request, and the code check is what guarantees the behaviour. The model's wording is no longer what the shopper sees, but the check is a word list, so it can miss phrasings I didn't anticipate.

The two reported cases now come out as blank reasons. "Great sound for under 100" is cleared by the digit and "under", and "Our top-rated cable" by "top" and "rated".

I made three judgement calls you may want to change:
- **"Best sound" is still allowed.** The existing test treats it as a valid reason, and it describes the product rather than comparing it with others. Blocking "best" would also remove most useful reasons.
- **"Cheap" and "budget" are still allowed as plain descriptions.** The existing test expects "Light and cheap" to pass, and a vague adjective isn't a figure a shopper can check. "Cheaper" and "cheapest" are blocked because they are comparisons.
- **Any digit blocks a reason,** including product specs like "2 m". That is blunt, but it avoids any stated price or rating slipping through.

The project is not a git repository, so I have not committed anything. The fix does not change reasons that have already been shown to customers.