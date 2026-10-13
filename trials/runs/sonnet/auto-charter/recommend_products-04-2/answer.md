I've made the part of this fix I can make, but it doesn't guarantee what you asked for. A guarantee needs a decision from you, set out below. The tests pass.

**What I changed**
- In `seam.py`, the prompt now tells the model that the price and rating are shown next to its reason, so the reason must agree with the listed figures.
- It must not state or imply a price, rating or comparison ("under 100", "top-rated", "cheapest") unless it is true by those figures, judged against every product in the list. When in doubt it should leave the figure out.
- In `test.py`, I added a test that the instruction reaches the model.

**What this does not do**
This is guidance, so the model can still get it wrong. The charter makes the wording of each reason a free decision of the model, and the code only constrains the length. The price and rating fields are always correct, because they come from the catalogue. The sentence under them is the model's own text, and nothing in code checks it.

**The line, and what moving it would buy**
Guaranteeing that "the Aria never appears with a promise of under 100" means code has to check or replace the reason. Any of these takes over a decision the charter lists as free:
1. **Check the reason in code.** Drop or blank any reason that mentions a number, or a comparative like "cheapest" or "top-rated", that doesn't match the catalogue. This is the closest fit, and a check on figures and superlatives is cheap. It does reject some honest reasons.
2. **Have the model write reasons without figures.** Forbid prices, ratings and comparisons in reasons entirely, then enforce it with a check. This is simpler and fully safe, but the reasons become blander.
3. **Build the reason from catalogue data by template.** This is fully safe, but the model no longer writes the reason.

Option 1 or 2 is what I'd recommend. Charter edits are yours to make, and I haven't touched the charter. If you tell me which option you want, I'll implement it once you've updated the charter.