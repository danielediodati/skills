The prompt now asks the model for reasons that are complete sentences under 80 characters. The unit tests pass (14 of 14), but I haven't confirmed the fix on real output because that needs a paid model run.

**What changed**

- `seam.py`: the prompt tells the model each reason must be a complete sentence of under 80 characters, so it ends on its own and never trails off. The limit comes from `MAX_REASON_CHARS`, so the prompt and the code can't drift apart.
- `test.py`: a new test checks that the prompt carries that instruction. It uses the fake model, so no paid call runs.

**Why it's in the prompt**

The charter leaves reason wording to the model and keeps the 80-character cap in code. Code can't turn a cut-off sentence into a complete one, so the wording has to come from the model. The cap and the truncation are unchanged: code still cuts anything over 80 characters as a safety net. A reason the model writes well but that is still too long will be cut, so the prompt change lowers the odds of a broken sentence without guaranteeing it.

**What I didn't do**

- I didn't change the charter or move any line. The instruction informs the model's wording; it doesn't take the decision from it.
- I didn't cut at word boundaries. That would still leave sentences like "...a whole" unfinished, so it wouldn't meet your goal.

**Next step: a paid check, needs your approval**

To see whether the model actually keeps reasons complete, I'd run the two queries from your report (the Aria and Pico results) plus a few more. Each invocation is one model call. Proposed budget: about 10 calls, roughly 2 per query across 5 queries. Please confirm that budget, or give me a different one, before I run anything.