The strip can now come back empty, but whether "kettle" actually gets nothing depends on the real model following the new prompt. I haven't run it against one. The 15 tests pass, but they use a fake model.

**Cause:** the prompt told the model to pick products that "best match" the search. When nothing matched, it still had to fill the list. It justified the picks with generic reasons like "popular choice", "highly rated" and "great value", which is what you saw.

**Change in `seam.py`:**
- The prompt now asks for products that "genuinely suit" the search. It says popularity, rating or price alone aren't reasons, and that fewer picks than the limit is fine.
- It tells the model to answer exactly `NONE` when nothing suits: an item you don't sell, an unrecognisable misspelling, or a brand you don't carry.
- Reasons must say why the product suits this search.

`NONE` already parsed to an empty list, so the parsing code didn't need to change.

**Tests and README:** I added a test that a `NONE` answer gives `[]` and one that the prompt carries the new instructions. I also documented the behaviour in `README.md`.

**Decision for you:** the function now returns an empty list for "kettle". The page should hide the "Recommended for your search" strip when the list is empty. The page code isn't in this folder, so I couldn't check that it does.

**Limit of this fix:** relevance is still judged by the model. A misspelling like "headfones" should still map to headphones, but a model that ignores the instruction could still pad. If you see that in practice, the next step would be a code-side check, such as requiring the model to cite the query term it matched.