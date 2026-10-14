I made the part of the fix that the charter allows, but it does not guarantee a reason on every card. The guarantee would need a line the charter sets in code, so that decision is yours.

**What I changed**

In `seam.py`, the prompt now says: "Every line needs a reason after the |, even for a looser match, so the customer can see why it was picked." The `ID | reason` format and the parser are unchanged. The charter lists the reason's wording as free and the prompt wording as changeable, so this stays inside it. The 13 existing tests still pass. I did not run the model, since that costs money and needs your approval first.

**Why it isn't a guarantee**

Your example has an empty reason for the earbuds and the cable. The charter says a pick with no `|` is accepted with an empty reason. The model can still leave the `|` off, and the prompt change only makes that less likely. Two ways to make it certain both move a line:

1. **Drop any pick with no reason in code.** This changes the charter's "accepted with an empty reason" constraint. The strip would then sometimes show fewer than three products, and the charter currently says that is fine.
2. **Fill a blank reason with fallback text in code**, such as "A good match for your search." This takes over the wording, which the charter gives to the model.

A second model call to write missing reasons is also possible, but the charter caps the budget at one call per search, so that would be a third line to move.

I think option 1 fits your goal best, since a card with no reason is the thing you want gone. The charter is yours to change, so I left it and the code's empty-reason behaviour as they are. Tell me which option you want and I'll make the change and update the tests.

**Also worth knowing**

I can't see the model's raw answer for yesterday's search, so I can't tell whether the earbuds and cable lost their reasons to a missing `|` or to a blank reason after it. A paid run with the same search would show which, if you approve one.