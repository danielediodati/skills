I haven't changed anything, because this request moves a line the charter draws on purpose, and that decision is yours.

**What conflicts** (`evals/recommend_products/charter.md`):
- Free: "How many, from none to `limit`: three that fit beat five that fill." The model is meant to return fewer than five when fewer fit.
- Constrained: "No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip."

Filling with the best-rated in-stock products overrides both. It is also the fallback list the charter rules out, and it would apply to the completely empty strip as well.

**Two things to settle with you:**
1. **Do you want to reverse that decision?** Your goal is a full strip, labelled "You may also like", with the fillers distinguishable. That is a coherent product call, but it replaces "empty beats unrelated". If you agree, I'd change the charter in the same commit so the model's selection stays free and code adds a clearly marked filler tier.
2. **Is the model returning too few for the right reason?** Two cables out of forty-plus suggests the model is being too conservative, not that only two fit. That is a prompt issue, which is separate and might shrink the problem without any filler. I'd like your call on whether to look at it as well.

**Proposed design if you approve:**
- Each returned item gets a `source` field, `"recommended"` or `"filler"`. Fillers have `reason: ""`.
- After the model's picks, code appends the best-rated in-stock products not already in the strip, highest rating first, up to `limit`. Ties are broken by catalogue order.
- The real picks keep today's order and come first.
- It stays one model call. The blank-search and nothing-in-stock cases still return `[]` without calling the model, since there is no search to fill for.
- The charter's "Free", "Constrained" and output lines, the README and the tests are updated together.

Should fillers also appear when the model returns nothing at all? Your second example suggests yes, and I'd assume so unless you say otherwise.