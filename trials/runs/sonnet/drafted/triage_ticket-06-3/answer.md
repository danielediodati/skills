I changed the prompt to tell the model to keep private details out of the summary. That is not a guarantee, and I stopped short of the part that would be one.

## What I changed
- **`seam.py`:** the prompt now says the summary appears in a list many people see, so it must not repeat card numbers, security codes, passwords or other credentials. It tells the model to name the kind of thing instead of its value. This is guidance for the model's judgement. It doesn't dictate an answer, so the summary wording stays the model's decision.
- **`test.py`:** one new test checks that the instruction reaches the model. All 12 tests pass locally, and I made no paid calls.

## What the prompt cannot do
A prompt asks for the behaviour, and the model can still slip. The next oversharing customer could still produce a summary with a number in it. I have not measured how often that happens, because that would need a paid eval run.

Two other places can still carry a secret:
- **Subject fallback:** if the model gives no summary, the subject is used, and customers put secrets in subjects too.
- **Hard 120-character cut:** the cut is applied to whatever the model wrote, with no check on what it contains.

## The line that stops me
The charter lists summary wording as free: "code only cleans and caps it". A guarantee has to live in code, such as a pattern filter for card-like digit runs or a deny-list that blanks or replaces the summary. That makes part of the summary's content a code decision. It also removes a decision the charter gives the model, so I can't add it, and I can't edit the charter.

- **What moving it would buy:** a deterministic floor. A card-like number or a known credential pattern could never reach the list, the wall screen or the manager report, whatever the model does.
- **What it would cost:** code-side filters only catch what they can pattern-match. A card number is easy, but a password like `Tulip-Harbour-92` is not. The filter would give a false sense of completeness for that case.

## Decision for you
Whether to move that line is your call. If you do, the charter needs a new "Constrained" entry for it. Tell me the rule you want and I'll implement it.

I'd also suggest measuring the prompt change first. I'd need a spending budget agreed with you before any paid call, for example a small set of 20–30 oversharing tickets (cards, passwords, API keys, addresses) on the cheapest model. Say if you want that and what budget you'd set.