The strip should now come back empty for searches like "kettle", but I haven't confirmed that with the real model. The fix is a prompt change, and the unit tests only check the prompt text.

**What was wrong:** The prompt said "Pick up to 5 products from the list that best match the search" and never told the model it could pick none. Haiku filled the slots with the closest thing in stock. The charter already keeps the "nothing fits" decision with the model, so the fix belongs in the wording.

**What I changed** (`seam.py`, prompt only):
- "Pick up to {limit} products" now reads "...that genuinely suit this search".
- Added: "The shop does not stock everything people search for. If no product in the list genuinely suits the search, pick none and answer with no lines."
- The answer-format line is untouched, since the parser depends on it. The code logic is unchanged.

**Tests:** I added `test_model_is_told_it_may_pick_nothing` in `test.py`. All 14 tests pass with `python -m unittest`.

**Not done:**
- **Real-model check:** I haven't run the model on "kettle" or your other misspelling and brand searches. That is a paid call, so it needs your approval and a budget first. The repo also has no model client, so I'd need you to point me at one. Suggested check: a few non-stocked searches plus a few that should still return picks.
- **Charter:** I didn't touch `evals/recommend_products/charter.md`, as AGENTS.md requires.
- **Page rendering:** An empty list is now a normal result. The storefront should hide the "Recommended for your search" heading in that case. That template isn't in this repo.