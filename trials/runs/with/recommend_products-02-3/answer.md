I haven't changed anything yet, because this request moves a line the charter draws on purpose, and `AGENTS.md` says that decision goes to you first.

**What conflicts in `evals/recommend_products/charter.md`:**
- **Free:** "How many, from none to `limit`: three that fit beat five that fill." The model decides how many products suit the search. Padding to five with best-rated stock takes that decision away from the model.
- **Constrained:** "No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip." Your second example, the completely empty strip, is exactly this case. Under your request it would show five best-rated products unrelated to the search.

**Why the charter may be part of the cause:** the `usb-c cable` search returned two products when forty exist. The charter lets the model return fewer than `limit`, and the prompt says "up to {limit}". The model is probably being too conservative, which is a separate problem from the strip layout.

**Proposed change, if you confirm the line moves:**
- `recommend_products` keeps the model picks first and in the same order. It then appends the best-rated in-stock products not already picked, highest rating first, until it reaches `limit` or runs out of stock.
- Tie-break on equal rating: catalogue order.
- Each returned item gets a `"filler": True/False` field so the front end can tell them apart. Fillers get `reason: ""`.
- The model is still called once, and a blank query or empty stock still returns `[]` without a call. For a blank query, fillers would not be added, because there is no search to pad.
- The charter is updated in the same change. The "Free" bullet on count becomes "how many real recommendations". The "no fallback" constraint is replaced by "the strip is filled with best-rated in-stock fillers, marked and without a reason". I would also update the README and add tests.

**Two questions:**
1. Do you accept that an unrelated search (the empty-strip example) now shows five fillers, labelled "You may also like"? Or should fillers appear only when the model returned at least one real pick?
2. Should I also tell the model in the prompt to be more generous with picks, so the `usb-c cable` case returns five real cables rather than two plus fillers? That would be a prompt change within what the charter calls free, so it doesn't move the line, but it would fix the underlying problem for searches like that.

Tell me which way you want to go and I'll make the change.