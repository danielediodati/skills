# Principles for splitting work between a model and code

1. The model owns judgment over open-ended input: reading meaning, weighing how serious something is, choosing a category, writing prose. Code cannot enumerate these cases, and rules written for them are brittle.
2. Code owns anything that is a policy, a contract, a promise to a customer or a fact about a business rule. These must be identical on every run, auditable, and changeable by someone with authority, not by a prompt.
3. Code owns the shape of the output: allowed values, types, lengths, and the mapping from one value to another. Whatever consumes the output depends on this, and a model cannot be trusted to hold it every time.
4. Code owns validation and fallbacks. Model output is untrusted input: parse it leniently in form, check it strictly in content, and never let an invalid value through.
5. Code owns the budget: how many calls, how much context, what is refused before spending a call.
6. Do not make code re-judge what the model decides. Code that overrides the model on meaning by keywords or heuristics is a worse model. Code may only adjust it by an explicit policy.
7. A fallback is a decision too. It must be chosen on purpose, be safe in the direction that matters, and should not be indistinguishable from a real answer.
8. Anything the model should not decide (facts it is given, such as customer tier) should be handled by code rather than put in the prompt for it to weigh.
