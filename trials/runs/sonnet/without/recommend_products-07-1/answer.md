The strip can now come back empty, so a search like "kettle" should no longer produce recommendations. All 15 tests pass, but they use a fake model, so nothing has been checked against the real one yet.

**Cause:** The prompt told the model to "pick up to N products that best match", so it always had to pick something. For "kettle" it filled the strip with the most popular or best-rated items and wrote generic reasons.

**Changes in `seam.py`:**
- **Prompt:** The model must pick only products that genuinely suit the search, or a close substitute. It is told not to pick on popularity, price or rating alone, and fewer picks is fine.
- **`NONE` answer:** If nothing suits the search, the model answers `NONE`, and the function returns an empty list. This also covers misspellings and brands you don't carry.
- **Reasons:** Each reason must now say why the product suits the shopper's search.
- **Stray picks:** If the model says `NONE` and then lists products anyway, the list is still empty.

**Tests and README:** I added tests for the `NONE` answer and for the prompt wording, and updated the README to describe the behaviour.

**Your page needs a change too:** The function now returns `[]` for these searches, so the page has to hide the "Recommended for your search" heading when the list is empty. Otherwise shoppers will see a heading with nothing under it. That code isn't in this folder, so I haven't changed it.

**Limit:** Relevance is still judged by the model, so an occasional borderline pick is possible. To check it, run a few unstocked searches ("kettle", a misspelling, an unstocked brand) through the real model.