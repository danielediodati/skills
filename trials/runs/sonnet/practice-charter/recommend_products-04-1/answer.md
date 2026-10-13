I haven't changed anything, because the fix you want crosses a line the charter fixes. Only you can move that line.

**The cause**

`evals/recommend_products/charter.md` lists the wording of each reason as a free decision for the model:

> The wording and angle of each reason... Nothing checks it against the catalogue, so it may claim things the model was never given. Assumed.

`seam.py` follows that. Price, rating and name are always read from the catalogue, but the reason is the model's text, passed through after whitespace collapse and the 80-character cut. So "under 100" next to 129.00, or "top-rated" next to a 4.4 when a 4.6 is in the strip, gets through. The model sees the real figures in its prompt and still sometimes contradicts them.

**Why I stopped**

Making the line reliable means one of two things, and both move the charter's line:

1. **Check the reason in code.** Reject or blank any reason that states a price, a rating, or a comparative ("cheapest", "top-rated", "under 100") that disagrees with the catalogue. This moves a wording decision from free to constrained. It is the only option that actually guarantees the Aria never shows "under 100", but it needs a rule for what counts as a claim. A check on figures is easy. A check on "best value" or "top-rated" is fuzzier.
2. **Build the reason in code.** Use a template such as "4.7 rated, 129.00", or let the model choose only an angle from a closed menu. This is a guarantee too, but it takes over the persuasive wording the charter leaves to the model.

A prompt instruction like "don't state figures that disagree with the list" would reduce the problem but not guarantee it, and it also narrows the free wording. I didn't add it, because you asked for reasons customers can rely on, and a softer prompt would still let the occasional "under 100" through.

**My recommendation**

Option 1, limited to what can be checked mechanically:
- Any currency figure or rating in a reason must match the product's catalogue value.
- Superlatives about rating or price ("top-rated", "cheapest", "best rated") must hold against the other products in the strip.
- A reason that fails is emptied, not repaired. The charter already says a pick with no reason is kept, with an empty reason, because the pick is the value.

That leaves the model's choice of products and their order untouched, and the strip never contradicts itself.

If you want that, update the charter to move the reason's factual claims into "Constrained" and tell me, and I'll implement it with tests for the Aria and USB-C cases. Or tell me you prefer option 2 or the prompt-only softening.