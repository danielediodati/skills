A reason line can no longer state or compare price or rating, so "Great sound for under 100" or "Our top-rated cable" won't appear. I couldn't run the tests after the last edit, because the shell was blocked partway through this session.

The last test run, before I fixed the patterns, showed 2 of 16 failing: the two new rule tests on word-boundary matching in the regex. I rewrote `seam.py` cleanly to fix that, and a check for stray control characters came back clean. I traced the new and existing test cases by hand and expect them all to pass. Please run `python -m unittest` to confirm.

## Cause
The reason is free text from the model, and the code passed it straight through. The model is given the price and rating but isn't forced to be accurate about them, and its wording is never checked against the figures.

## Fix, in `seam.py`
- **Prompt:** the model is now told not to mention prices, ratings, or how products compare on either. This is only a request, so it is not the safeguard.
- **Check on every reason:** a reason is rejected if it contains a digit, a currency symbol, or wording about price, rating or standing. That covers "under", "cheapest", "top-rated", "stars", "than", "bargain", "value", "hundred" and similar.
- **Fallback:** a rejected reason becomes an empty string, which the README already allowed. The product still appears with its real price and rating printed beside it.

## Trade-offs
- **Over-blocking is deliberate.** I can't verify free text, so I chose to drop a good reason rather than let a wrong one through. "Long 2 m cable" or "tangle-free" will also lose their reason. Reasons like "Comfortable over-ear fit with deep bass" pass. Relax the word list if too many reasons go blank.
- **Blank reasons.** Some picks will show no line under them. Say if you'd rather show a fixed, always-true fallback such as "Matches your search".

## Other changes
- **Tests:** I added tests for price claims (including the Aria "under 100" case), rating and standing claims (including the 1 m cable "top-rated" case), and a reason that should survive. I changed "cheap" to "portable" in existing test strings, since "cheap" is now filtered.
- **README:** it now documents the rule.