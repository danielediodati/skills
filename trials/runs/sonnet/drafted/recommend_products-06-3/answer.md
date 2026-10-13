I made the part of this that is mine to make, but it can't guarantee the outcome you asked for. The guarantee needs a decision from you.

## What I changed
`seam.py` now tells the model, in the prompt, that the customer sees the reason under each product, so every line needs one. It also says a partial fit should be explained by what it offers this search, and that a product the model can't give a reason for should be left out. I added a test that the prompt carries this instruction. The unit tests pass (14), and nothing paid was run.

The prompt change should make blank reasons rarer. It is a request to the model, so it can't promise there are none. I haven't measured it: checking it would take a paid eval run, and I'd need your approval and a budget first.

## The line I can't cross
The charter for this seam, `evals/recommend_products/charter.md`, says in Constrained: *"A pick with no reason is kept with `reason` `""`: a valid product is worth showing even if the explanation is missing; code does not call the model again or invent text."*

Guaranteeing a reason on every card in code means one of three things, and each overrides that line:
- **Drop picks with no reason.** The strip would show only explained products. In your example, that would likely leave only the Aria headphones. You'd never see an empty gap, but you might also never see the earbuds or the cable.
- **Re-ask the model for the missing reasons.** Each blank gets a second call, which costs one extra model call per blank and breaks the "exactly one model call, no retry" budget.
- **Fill in a stock line in code.** This is cheap, but it is generic text that doesn't explain why wired earbuds suit a wireless search.

## Your decision
Drop-or-keep is a trade between a possibly shorter strip and a possibly blank card. The charter currently chooses to keep. I'd recommend dropping reasonless picks if the shop cares most that the strip never looks broken. Re-asking is the best choice if you want those products explained, and it costs one extra call per blank. Tell me which you prefer, or whether to leave the charter as it is, and I'll go from there. Only you can change the charter.

I'd also like to see the raw model output for the "wireless headphones" search. If the model returned the earbuds with no text, the prompt change is the right fix. If it returned something the parser skipped or cut, such as `H-200: reason`, the fix is different.