I made the part of this that stays inside the charter, and stopped at the point where a full fix would move a line.

**What changed**

- `seam.py`: the prompt now tells the model that each reason must agree with the list. It may quote a price or rating only as shown, and must not call a product cheaper, dearer, better rated or top-rated than another. This is a criterion for the model's judgement, so it stays within the charter's free wording.
- `test.py`: one new free test checks that the prompt carries that instruction. All 14 tests pass.

I did not edit the charter, and I made no paid model calls.

**What this does not guarantee**

The prompt instruction makes the model less likely to write "Great sound for under 100" or "Our top-rated cable". It cannot make it certain. The model may still get it wrong, and the code will still pass the text through unchecked. I could not measure how often that happens, because checking would need a paid eval run.

**The lines that would need to move for a guarantee**

1. **Code checks reason content.** The code would reject or strip reasons that contain prices, ratings or comparative claims. The charter says code checks only length and line shape, and does not check content or accuracy. Taking that on moves the line.
2. **Code writes the reasons.** Reasons could be built from catalogue facts in code, so the model no longer writes them. The charter lists reason wording as free to the model, so this moves that line too.

Either option gives a deterministic guarantee. Option 1 is the smaller change, but it is a rule-based text filter that may reject good reasons. Option 2 is the strongest guarantee, but it removes the model's prose from the strip. The choice is yours, since only you can change the charter.

**Next step, if you want one:** I can run a small paid eval on the prompt change, using the Aria and cable cases. I would need your approval and a spending budget for the ticket first.

This directory is not a git repository, so I did not commit anything.