I made the part that can be made. It is not a full guarantee, and the rest needs your decision.

**What I changed**
- `seam.py`: the prompt now tells the model that the reason must be one complete sentence of at most 80 characters, because it is shown on one line and anything longer is cut off. The number comes from `MAX_REASON_CHARS`, so it follows the display limit if you change it.
- `test.py`: one new test checks that the limit reaches the model.
- The 14 local tests pass. No paid calls were made.

The model was never told the limit, so it wrote long sentences and the code cut them mid-word. Telling it should make most reasons fit. The wording stays the model's.

**What this does not guarantee**
The model can still overshoot, and the code will then cut that reason mid-word. The charter fixes that cut as hard, with no ellipsis and no word boundary, and I may not move that line.

**The line, and what moving it would buy**
Making every shown reason complete takes a code rule for what happens to an overlong reason. These are the options:
- Cut back to the last word boundary. The reason never ends mid-word, but it can still stop short of the point, as in your Pico example.
- Cut back to the last full sentence. Reasons always read as complete, but an overlong one-sentence reason would become empty.
- Drop an overlong reason to `""`. This is the same outcome as the sentence option for a single long sentence, and the UI must already handle empty reasons.

Sentence-level trimming is the only one of these that matches "a complete thought". Tell me if you want to change the charter that way and I'll implement it.

I have not run the real model against the new prompt. If you want to measure how often it still overshoots, that is a paid run and needs your approval and a budget first.