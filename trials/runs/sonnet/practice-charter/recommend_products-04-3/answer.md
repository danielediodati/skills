I made a partial fix, and it can't give you the guarantee you asked for. The full fix needs a decision from you.

**What I changed**
- `seam.py`: the prompt now tells the model that its reason is shown next to the real price and rating. It must not state or imply a price, price threshold, rating or comparison ("cheapest", "top-rated") unless the listed figures bear it out.
- `test.py`: added a test that the instruction reaches the model. All 14 tests pass.

This should make bad lines like "under 100" on a 129.00 product much rarer, but it is only a request to the model. Nothing in code enforces it, so the Aria could still appear with a wrong promise.

**The line that blocks the full fix**
The charter in `evals/recommend_products/charter.md` lists the wording of each reason as free to the model. It says outright that nothing checks reasons against the catalogue. Making your guarantee hold means code deciding what a reason may say, which moves that line. I can't edit the charter or move the line myself.

**Options for you to choose from**
1. **Code check on reasons.** Code rejects or blanks any reason that contains a number or a ranking claim that disagrees with the catalogue. The guarantee becomes real, and the model still writes the prose.
   - The catch is that reasons will sometimes be blanked or dropped.
   - Code can detect numbers fairly reliably but ranking words ("our top-rated cable") only approximately.
2. **Code-built reasons.** Code writes the price and rating facts itself, and the model supplies only non-numeric wording. This is the strongest guarantee but takes most of the persuasive wording away from the model.
3. **Keep the prompt-only fix.** It costs nothing, but a wrong line can still slip through. That sits badly with your consumer-protection concern.

For the legal risk I'd recommend option 1, with blanking as the failure behaviour. The charter already treats an empty reason as acceptable ("the pick is the value, the reason is decoration"). If you update the charter to make reason accuracy a constrained decision, I'll implement it.