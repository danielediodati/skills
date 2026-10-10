I haven't changed anything. The request conflicts with the charter at `evals/recommend_products/charter.md`, and only you can move that line.

**The lines in the way**
- **Constrained:** "No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip." Filling an empty strip with best-rated products is exactly the fallback list this forbids.
- **Free:** "How many, from none to `limit`: three that fit beat five that fill." Topping up to five takes the count away from the model and turns it into a constant.

The strip is deliberately allowed to be short or empty today. The charter's reasoning is that an unrelated product costs more than a gap. Your request reverses that tradeoff, with a lower-risk variant: fillers are flagged and labelled "You may also like", so the shopper isn't told they match the search.

**What moving the line would buy**
- The strip is always full whenever enough products are in stock, and no search leaves the top row empty.
- Each product would carry a marker such as `"filler": True`, with an empty reason, so the UI can show the "You may also like" label.
- Real recommendations would stay first, in the model's order. Fillers would be best-rated in-stock products not already picked, highest rating first.
- It would cost nothing extra: no extra model call, and the model's own picks are untouched.

**What it would take from you**
- Edit the charter yourself: drop or rewrite the "no fallback list" line and the "three that fit beat five that fill" line. A rewrite could say fillers are allowed but must be flagged and always come after model picks.
- Then I can implement the fill step in `seam.py`, update the README, and add tests for the fill order, the flag, and the blank-query and nothing-in-stock cases.

One open question for that rewrite: should a blank search or an out-of-stock catalogue still return an empty list (as the mechanical-steps line says), or should a blank search also show fillers?

Separately, if two-of-five on `usb-c cable` is the model returning too few when forty cables fit, that is a prompt or model-quality issue within the free zone. I can investigate it without touching the charter, if you want.