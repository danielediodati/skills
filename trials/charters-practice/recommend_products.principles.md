# Principles for splitting work between a model and code

1. The model owns judgment that has no checkable right answer: relevance, ranking, taste, wording, tone. Code cannot enumerate these rules, and writing them in code makes them brittle.
2. Code owns every fact that exists in a system of record: IDs, names, prices, stock, ratings. The model may refer to a fact, but code supplies it. A model-written fact is a possible lie.
3. Code owns invariants that must hold on every run: what may be shown, how many, how long, no duplicates, no invented items. Anything checkable by a cheap deterministic test is checked in code, after the model, whatever the prompt says.
4. A prompt instruction is a request, not a guarantee. Anything the product depends on is enforced in code as well as asked for in the prompt.
5. Code filters before the model for cost and safety (never offer what must not be returned; skip the call when the answer is known), and validates after it.
6. Be tolerant in parsing, strict in what leaves. Accept harmless format noise from the model; never pass unvalidated model output on.
7. When model output is partly unusable, drop the bad part. Do not fill the gap with code-made guesses that look like model judgment.
8. Failure policy (empty result, retry, error, fallback) is a product decision and belongs to code, in the open, not to the model and not to an accident of parsing.
9. Bound what goes into the model: every unbounded input is a cost and context risk that code must cap.
10. A decision that sits in code only by accident is still a decision: name it and put it on the side its nature gives it.
