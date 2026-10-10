I made the part of this that fits the charter, and stopped short of the guarantee you asked for.

**What I changed**

In the prompt in `seam.py`, I added one line: "If a reason mentions a price, it must be exactly the price listed for that product." This should make wrong prices rarer, but it cannot guarantee that none go out, because the model can still ignore it.

**The line I did not move**

Your guarantee needs code that reads each reason, finds any price in it, compares it to the catalogue price, and blanks the reason on a mismatch (keeping the product). The charter rules this out in two places:

- Under *Free*: "What each reason says… claims in it are not checked." The content of the reason belongs to the model.
- Under *Constrained*: the only things code does to a reason are cutting it to 80 characters and keeping an empty one. Nothing there lets code rewrite or blank a reason based on what it says.

A price check would be a code check on what a reason claims, which is the decision the charter leaves to the model. Only you can change that.

**What moving it would buy**

- A guarantee: no reason ever states a price other than the product's actual one.
- The product stays in the strip with an empty reason, which the charter already allows.
- The cost is that code would start judging reason content, so the charter's "claims are not checked" would become "price claims are checked".

If you want that, update the charter (a price claim in a reason is checked against the catalogue, and a mismatch blanks the reason). I can then implement it in `seam.py` and add tests for the two examples you gave, the 19.90 earbuds and the 9.50 cable.