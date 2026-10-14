The strip now shows only products the model judges to suit the search, and returns nothing when none do. For "kettle" it returns an empty list, so the page shows no strip. All 15 unit tests pass.

**The cause:** the prompt in `seam.py` asked the model for "up to N products" and never allowed it to pick none. The model therefore always filled the strip, and the "popular" and "highly rated" reasons were its way of justifying products that didn't match.

**What I changed:**
- **`seam.py`, prompt:** the model may now answer `NONE`. It may only pick products that the customer would plausibly want for what they typed (the thing itself, a close variant, or a direct accessory or alternative), and it must not pick something because it is popular, highly rated or good value. It should allow for misspellings. Reasons must say how the product fits the search.
- **`test.py`:** two new tests. One checks that a `NONE` answer gives an empty list. The other checks that the prompt carries the no-match instruction.
- **`README.md`:** documents that an empty list is a valid result and that the caller should hide the strip then.

**What I could not verify:** the matching now depends on the model's judgement, and the tests use a fake model. I haven't run this against the real model, so I can't confirm how it handles borderline cases such as misspellings or a brand you don't carry. It's worth running the kettle, misspelling and unknown-brand searches through the live model before relying on it.

**Still to do outside this repo:** the "Recommended for your search" heading and the page code live in your shop front end, which isn't in this folder. That code needs to hide the whole strip, heading included, when `recommend_products` returns an empty list.