I added only part of this. The guarantee you asked for is not in place.

**What I changed:** in `seam.py` the prompt now says that if a reason mentions a price, it must be exactly the price listed for that same product. This should make wrong prices rarer, but nothing enforces it, so a wrong price can still go out.

**The line I stopped at:** the guarantee needs a code check that finds prices in the reason and blanks the reason when one differs from the catalogue price. The charter at `evals/recommend_products/charter.md` lists "what each reason says" as free, and says "claims in it are not checked". A price check in code is exactly such a check, so adding it moves that line. Only you can change the charter.

**What moving it would buy:**
- A wrong price could never reach a shopper.
- The product would stay in the strip with an empty reason. The charter already supports that: "the right product without a reason beats no product".
- It would be a small code change: extract numbers that look like prices (€14.90, $4, 19,90), compare them to `product["price"]`, and blank the reason on a mismatch. Numbers like "2 m" or "30-hour" would be left alone.

If you want it, update the charter so price claims in reasons are constrained, or tell me to go ahead on that basis, and I'll add the check and tests.