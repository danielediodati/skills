I changed the prompt in `seam.py` so the model is told it may recommend nothing, and the local tests pass. I have not run it against a real model, so I can't yet confirm "kettle" now returns an empty strip.

**Cause.** The prompt said "Pick up to N products that best match the search". With no instruction to leave anything out, the model filled the strip with the best of what was left. It then wrote a reason from price and rating, which is why the reasons never mention the search.

**Change.** The prompt now asks for products that *genuinely suit* the search. It tells the model not to pick something just because it is popular, cheap or well rated, and to answer with nothing if nothing suits.

The charter lists "how many, from zero up to `limit`" and "which products suit the search" as the model's free decisions. The new wording only gives the model the criterion and permission to return zero. It adds no code filter, so no line moved and I did not touch the charter.

I also added a test that an empty model answer returns `[]` and that the prompt contains the "nothing suits" instruction. All 14 tests pass.

**Still open:**
- **Page copy:** the "Recommended for your search" heading is outside this code. For an empty result the page should hide the strip entirely, which is a front-end change.
- **Real-model check:** a few queries such as "kettle", a misspelling, and an uncarried brand would confirm the model now returns nothing while real searches still fill. That is a paid run, so I haven't done it. If you want it, tell me a budget and I'll propose the cases and cheapest model first.