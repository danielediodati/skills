I changed the prompt so the model is allowed to return nothing when no product fits the search. The 13 local unit tests pass, but I have not checked the fix against the real model, so I can't yet say "kettle" will now show an empty strip.

**What was wrong:** The prompt in `seam.py` said "Pick up to {limit} products ... that best match the search." It never said the model could pick none, so it always filled the strip with its least-bad guesses. That is what produced headphones and cables for "kettle".

**What I changed:** The prompt now asks for products that genuinely suit the search, including close alternatives such as synonyms. It says that if nothing suits, the answer should be empty. It also asks each reason to say how the product suits this search, which addresses the generic "A popular choice with our customers" reasons.

**Charter and code:** I did not touch `evals/recommend_products/charter.md`. The charter already leaves relevance, the number of picks, and reason wording to the model, and the prompt change fits that. The code-enforced parts are unchanged: the stock filter, the ID check, the limit, and the 80-character cap. Code can't judge relevance, so there is no code-side fix for "kettle" that stays within the charter.

**Not done:** Checking the real effect needs a paid model run, and the project rules require your approval and an agreed budget first. A reasonable check would be a small set of queries: "kettle", a misspelled brand, and a few that should still return results. Tell me the budget and I'll propose the run with the running total.