A reason line that contradicts a product's figures is now blanked before it reaches the strip, so the Aria can no longer appear with "under 100". All 20 tests pass, including the two cases from your report. The changes are in `seam.py`, with new tests in `test.py` and a note in `README.md`.

## What changed

- **Prompt:** the model is now told not to state or hint at price, rating or comparisons, since those are shown separately. This lowers how often the problem occurs but does not guarantee anything.
- **Check on every reason:** after the picks are final, each reason is compared against the figures shown for that product and against the other products in the returned strip. The check covers the text actually shown, after the 80-character cut.
  - **Prices:** "under 100", "over 100", "€129" and "only 99" are checked against the real price. "Under 100" on a 129.00 product is a mismatch.
  - **Ratings:** "4.9/5", "rated 4.8" and "over 4.5 stars" are checked against the real rating.
  - **Standing:** "cheapest", "most expensive", "top-rated" and "lowest-rated" must hold within the strip. "cheap" and "affordable" require the price to be at or below the strip's median. In your example, the 1 m cable with "Our top-rated cable" now gets an empty reason, because the 2 m cable is rated higher.
  - **Unverifiable comparisons:** "cheaper than the others" and "best value" are blanked.
- **Numbers that are not prices or ratings** are left alone: "30 hour battery", "1 m braided", "under 2 m of slack".

## Behaviours to know about

- **Failure shows nothing.** A reason that fails the check comes back as `""`, not a rewritten one. Your front end should handle an empty reason line gracefully.
- **"Top-rated" is judged against the strip, not the whole catalogue.** That matches "what the shop actually shows". With a one-product strip, "top-rated" will always pass. Say if you want it compared against all in-stock products instead.
- **The check is pattern-based and errs toward blanking.** Unusual phrasings such as "a hundred" or "one of the lowest prices" could slip through, and an innocent phrase like "5-star build" will be blanked. If you want a hard guarantee, the stricter option is to blank any reason that mentions money or ratings at all, or to generate the price/rating wording ourselves from the data and drop the model's version.

## Shell quirk

Some of my shell edits wrote stray backspace characters into `seam.py`. I rewrote the file in full, and the tests confirm it is clean.