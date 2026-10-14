Every product in the strip now has a reason under it. A product the model gives no reason for is left out, and the next pick takes its place.

The cause was in `seam.py`: the model sometimes returned a product ID with no reason after the `|`, and the code passed that product through with an empty reason. That is why the Pico earbuds and the 2 m cable showed blank gaps.

Changes, all in `<work>\charter-trial\haiku\without\recommend_products-06-3`:

- **`seam.py`**: the reason is cleaned up first, and a pick with an empty reason is skipped. Skipped picks don't count toward `limit`, so the strip still fills up from the model's remaining picks.
- **`test.py`**: the test that expected an empty reason now expects the product to be left out. I added a test where a blank pick is followed by a good one, and the good one takes its place.
- **`README.md`**: one sentence describes the new rule.

All 14 tests pass (`python -I -m unittest discover`).

I chose to drop these products rather than fill the gap with generic text such as "Rated 4.1 out of 5". A generic line would still not explain why the earbuds suit a wireless-headphones search.

The trade-off: if the model gives few reasons, the strip can show fewer than three cards, or none. If that happens often, the fix belongs in the prompt or in a retry, which I haven't changed. The directory isn't a git repo, so I didn't commit anything.