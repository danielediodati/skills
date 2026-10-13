I made part of the fix, but it can't guarantee what you asked for. Getting the guarantee means moving a line in the charter, and that decision is yours.

## What I changed
`seam.py`: the prompt now tells the model that the shop prints each product's price and rating beside its reason. It says that anything the reason claims about price, rating or comparison with the other products must be true of the listed figures, and that it should leave a claim out when unsure. The 13 local tests pass. I ran no paid calls.

## Why this isn't a guarantee
The charter lists the wording of reasons as a free decision for the model, with code fixing only length and shape. A prompt instruction informs the model's judgement and stays inside that line, but it is a request. The model can still write "under 100" next to a 129.00 price, and nothing in code would catch it.

A guarantee needs code that checks each reason against the catalogue figures. That means one of two things:
- **Reject or blank a contradicting reason.** The product stays and the line is dropped, or the product is dropped.
- **Replace the reason with text built from the catalogue.** This is fully safe but removes the model's wording.

Either one makes the content of the reason a constrained decision instead of a free one. That moves the line, so I stopped. Neither is a perfect check:
- Numeric claims such as "under 100" can be parsed and tested.
- Claims such as "our top-rated cable" or "cheapest" can only be checked by a fixed set of phrases, and paraphrases would slip through.

## Decision for you
Do you want to move the line so the reason's claims about price and rating are checked in code? If so, update the charter first. Then I can implement the check and its tests, and I'd suggest blanking the reason on a contradiction. The charter already allows a product with an empty reason.

Once the charter is updated, I'd also want to run a paid eval on the "wireless headphones" and "usb-c cable" cases to confirm the prompt change helps. I'll agree a budget with you before any paid call.