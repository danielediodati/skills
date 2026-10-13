I made the part of the fix that fits the charter. It lowers the chance of a wrong reason but does not guarantee the Aria never gets one.

**What I changed**
- `seam.py`: the prompt now tells the model that each reason is printed next to the product's real price and rating. It must not state or imply a price or rating the product doesn't have, and must not claim "cheapest" or "top-rated" unless the list shows it.
- `test.py`: added a test that the prompt carries this instruction. All 14 tests pass.

This is a criterion informing the model's judgement, so it stays within the charter. Because the model still writes the line, it can still get it wrong. The test only checks the instruction is in the prompt, not that the model obeys it.

**The line I did not cross**
The charter lists the wording of reasons as free for the model, and its guarantee that the model cannot misstate a price or rating covers only the structured fields, not the reason text. A hard guarantee would need code to inspect or override the reason, which takes that decision away from the model. I haven't done that, and I haven't touched the charter.

**What moving the line would buy**
Any of these would make "the Aria never appears with a promise of under 100" true by construction:
1. **Reject or blank reasons that contain a number or a comparative or superlative** ("under", "top-rated", "cheapest"). It is simple and fully checkable, but it would also drop harmless reasons and leave some picks with an empty reason.
2. **Have code write the price and rating phrases** and let the model write only the rest. This gives the most accurate output, but it constrains the reason's wording.
3. **Drop the reason line from the strip**, since the price and rating are already shown. This is the safest option, but the strip loses the tailored explanation.

Option 1 or 2 would need the charter's "wording of each reason" entry changed by you. Tell me which one, if any, and I'll implement it.