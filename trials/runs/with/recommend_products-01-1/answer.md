I haven't changed anything yet. This fix moves a line the charter draws, so it's your call, and the charter has to change in the same commit.

**Why it moves the line** (`evals/recommend_products/charter.md`):
- "Which products suit the search" is listed as free, so the model decides that today, price included. A price limit enforced in code takes part of that decision over.
- "The model sees every in-stock product; code does not narrow the catalogue before the call." This rules out the obvious fix of filtering the catalogue by price before the prompt.

**What I'd propose:**
1. **Parse the bound in code.** A small parser would read `under/below/less than/max/up to N`, `over/from N`, and `between N and M`, with optional `€`/`euro`. It returns a (min, max) range, or none if the search has no price.
2. **Filter the model's picks, not the catalogue.** The model still sees every in-stock product and still chooses and orders them. Code then drops any pick whose catalogue price is outside the range, before applying `limit`. If nothing survives, the strip is empty, with no fallback. This leaves the existing "model sees everything" rule intact and matches your "empty rather than too expensive" preference.
3. **Charter edit.** Add to Constrained: "A price limit stated in the search is a hard bound enforced on the picks: nothing outside it is returned. The model still sees the full catalogue." Also narrow the free "which products suit" line to say it operates within that bound.
4. **Tests.** Cover each phrasing (`under 50`, `below 50`, `max 30 euro`, `up to €30`, `less than 20`, `over 100`, `from 100`, `between 20 and 40`), a no-price query unchanged, and an empty strip when nothing fits.

**One side effect:** because picks are filtered after the model chooses, `limit` slots can be wasted on over-budget picks. For `headphones under 50` the model might return 5 picks and 3 get dropped, leaving 2 even though more in-range products exist. I can mitigate this by telling the model the parsed bound in the prompt so it picks within it, with the code filter as the guarantee. That is still one call, but it nudges a free decision, so it's part of what I'm asking you to approve.

Should I go ahead with the post-filter, with or without the prompt hint? Or would you rather keep price entirely with the model and tune the prompt only?