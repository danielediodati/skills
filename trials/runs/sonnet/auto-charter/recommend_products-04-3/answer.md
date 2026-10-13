I made the part of this fix that fits within the charter. It reduces wrong reasons but cannot guarantee they never appear.

**What I changed**
- **Prompt (`seam.py`):** it now tells the model that the shopper sees the price and rating above its reason. It must not state or imply a price, rating or comparison ("under 100", "top-rated", "cheapest") that isn't true of the listed figures, and should leave it out when in doubt.
- **Test (`test.py`):** one new test checks that the instruction is in the prompt. All 14 tests pass.

**Why this isn't a guarantee**
The charter lists the wording of each reason as a decision the model is free to make. Code only controls the price and rating fields, which come from the catalogue. The "Great sound for under 100" line sits in that free text, so the code never checks it. Only the model's own care keeps it consistent with the figures, and a prompt instruction can't promise "never".

**The line that would have to move**
A guarantee needs code to check each reason against the catalogue and act when it disagrees. That takes wording out of the model's hands. Options, from least to most intrusive:
1. Drop any reason that contains a number not matching the product's price or rating. This catches "under 100" on the Aria but not "top-rated", so it only partly solves the problem.
2. Replace reasons with a template built from the catalogue figures. This is fully safe, but the model no longer writes tailored reasons.
3. Have a second model call verify each reason. This breaks the one-call-per-request rule and is still not a guarantee.

For a price-accuracy and consumer-protection concern, I'd pick option 1 and accept that comparative claims stay a model judgement. Option 2 is the choice if you want it airtight. Either one changes the charter, so that decision is yours. Tell me which you want and I'll implement it once the charter reflects it.