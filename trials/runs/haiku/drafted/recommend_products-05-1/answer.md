I changed the prompt so the model is asked for a complete sentence of at most 80 characters. This should stop most reasons being cut, but it doesn't guarantee it, and I couldn't run the tests.

**What changed**
- `seam.py`: the prompt now asks for "one complete sentence addressed to the customer, at most 80 characters". It replaces "one short reason". The limit is filled from `MAX_REASON_CHARS`, so the prompt and the cut can't drift apart.
- `test.py`: one new test checks that the prompt carries the complete-sentence and 80-character wording.

**Why it isn't a guarantee**
The 80-character cut in code is a constrained decision in the charter (`evals/recommend_products/charter.md`, line 22), so I left it alone. If the model still writes a reason over 80 characters, it gets cut mid-word, as before. Making every reason complete means changing that line, for example by dropping over-long reasons or trimming them at a sentence boundary in code. That is your decision to make. I didn't edit the charter.

**Not verified**
The test run was denied by the session's permission check, so I didn't run the unit tests. I also made no paid model calls. The only check is reading the edited prompt back, which looks right. Please run `python -m unittest test` from the project folder to confirm.