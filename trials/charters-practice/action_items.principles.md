# Principles for splitting work between a model and code

1. Reading meaning is the model's: deciding what a text commits someone to, what refers to what, what a vague phrase most likely means. Code cannot enumerate these cases; rules written for them fail quietly on the first unusual input.
2. Facts, arithmetic and membership are code's: calendars, counting, sorting, comparing against a known list. Code is exact and free; a model is occasionally wrong and cannot be told apart from right. Code supplies the facts the model needs instead of expecting the model to know them.
3. Anything a downstream consumer relies on is code's: shape of the output, allowed values, limits, order. The model's answer is a proposal; code checks it and is the only thing the consumer should have to trust.
4. Code checks the model, it does not redo the model's job. A check that rejects, repairs or rewrites meaning (fuzzy matching, paraphrase detection, guessing a missing field) is a language decision sitting in code, and it fails on every input nobody anticipated.
5. A check should fail toward the least lossy result. Prefer keeping the item with an unknown field over dropping it, and never lose content silently when a cheap alternative exists.
6. A limit that the model is not told about is a silent loss. Limits enforced by code should also be stated to the model, so it spends its effort inside them; code stays the backstop.
7. Cost: one call per request by default; add calls or retries only for a decision that cannot be checked in code and whose failure is worse than the cost.
8. Where a line is a judgement call between two defensible places, pick the side that is cheaper to be wrong on and say so.
