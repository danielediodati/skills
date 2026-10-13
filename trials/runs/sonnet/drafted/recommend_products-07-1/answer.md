I haven't changed anything. The fix needs a change the charter reserves for you.

**Cause.** The prompt in `seam.py:7-14` says "Pick up to {limit} products from the list that best match the search". It never says that picking nothing is acceptable, so for "kettle" the model fills the strip with the closest-sounding items. The charter already lets the model return zero products (`evals/recommend_products/charter.md:8`), and the code already returns `[]` for an empty answer. The model just isn't being told it may.

**The line.** The fix is a one-sentence change to the prompt's instruction wording, along the lines of "If nothing in the list genuinely suits the search, answer with nothing." That kind of criterion informs the model's judgement and doesn't dictate an answer. But the charter's Constrained section (line 24) fixes the prompt shape, including "the instruction wording and answer format". Editing the wording moves that line, and only you can do that. I also can't edit the charter to record the change.

**What I deliberately didn't do.**
- A code-side relevance filter (keyword match, score threshold) would take over a decision the charter lists as Free, namely which products suit the search.
- Dropping picks whose reasons look generic would be the same problem. The charter also says reason content is not validated.

**What changing the line would buy.** With the wording changed, "kettle", misspellings and uncarried brands would produce an empty strip. The page could then hide the "Recommended for your search" heading when the list is empty. That is a caller-side change, outside this function.

**Decision for you.** Do you want the instruction wording opened up so the prompt can say "none is a valid answer"? If so, update the charter's line 24 (or tell me to proceed on that basis) and I'll make the prompt change and add a unit test. A real check that "kettle" now returns `[]` needs a paid model run, and I'd agree a budget with you before making any call.