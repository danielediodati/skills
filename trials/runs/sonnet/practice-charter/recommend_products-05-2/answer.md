I made the part of this fix I can make, and it won't fully guarantee what you asked for.

**What I changed**
- `seam.py`: the prompt now tells the model that each reason must be a complete sentence of at most 80 characters and shouldn't trail off. The limit comes from `MAX_REASON_CHARS`, so the two can't drift apart.
- `test.py`: a new test checks that the prompt states the limit. All 14 tests pass.

**Why cuts are still possible**
The model was never told about the 80-character limit, so it wrote longer sentences and code chopped them. Telling it should make most reasons fit. But a model can still overshoot, and when it does, code still cuts the text at 80 characters.

**The line I can't move**
The charter lists the cut as a constrained decision: "cut at 80 characters... The cut is mid-word, with no ellipsis." Only you can change that. Getting a hard guarantee that every reason reads as a complete thought means changing that rule. The options:

1. **Drop the reason when it's too long.** The product still shows, with an empty reason, which the charter already allows. This is the cheapest option and never shows a broken sentence, but the strip loses the reason for some products.
2. **Cut at the last sentence or word boundary.** This never ends mid-word, but it can still drop the point of the sentence, as in your Pico example.
3. **Ask the model to shorten an over-long reason.** This guarantees the best result but needs a second model call, which breaks the charter's budget of one call per search with no retries.

I recommend option 1 on top of the prompt change. If you want one of these, say which, and update the charter's "Reason length and shape" entry yourself, since I don't edit charters.