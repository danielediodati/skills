Every product in the strip now comes with a reason, or it doesn't appear. The change is in `seam.py`, and the 16 unit tests pass.

**What was happening:** when the model wrote a pick without a reason, `recommend_products` returned it with `"reason": ""`. The old test `test_pick_without_a_reason_has_an_empty_one` asserted that behaviour, so it was locking the bug in.

**What it does now:**
- If a pick has no reason, the function asks the model once more, with a separate prompt that names only those products. The prompt asks it to say what the product offers that's relevant, even if it isn't exactly what was searched for. That's the case of the earbuds under "wireless headphones".
- If a product still has no reason after that, it's left out of the result. The strip then shows fewer cards rather than a card with a gap.
- If every pick already has a reason, there's no second call.

**Tests:** I replaced the test that enshrined the empty reason. I added tests for the second ask, for the prompt naming only the missing products, for dropping a product that is still missing a reason, and for no second call when nothing is missing. `FakeModel` now takes several answers in turn so the second ask can be tested. I also added a sentence to `README.md` describing the guarantee.

**Choices you may want to change:**
- I dropped a product that still has no reason, rather than inventing a generic line like "Matches your search". A generic line would be shown as if it were a real reason.
- The strip can show fewer than `limit` products. The function takes at most `limit` picks before the reason check and doesn't go back for replacements. If you'd rather the strip always fill up, that needs a loop that asks for more candidates.
- The second ask costs one extra model call, only when some pick comes back without a reason.

I haven't run this against the real model, so I can't confirm what the earbuds' reason will say. The tests use a fake model.