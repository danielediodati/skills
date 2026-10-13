I made the part of this that I can make, and it does not give you the "never" you asked for. Getting to "never" needs a decision that is yours.

**What I changed**
- `seam.py`: the prompt now tells the model that the customer sees the price and rating directly above its reason. It also says that any claim about price, rating or standing against the other products must agree with the figures in the list, and otherwise be left out.
- `test.py`: one new test checks that the instruction reaches the model. All 14 tests pass. I ran no paid calls, so I haven't measured how much this reduces the bad lines.

**Why it can't be a guarantee**
The charter lists the wording and content of each reason as a free decision for the model, and says code "only trims it". The same charter does guarantee that the name, price and rating shown come from the catalogue, so the figures themselves are always right. Only the sentence underneath can disagree with them. A prompt instruction makes a contradiction less likely, but a model can still write "under 100" next to 129.00.

**The line, and what moving it would buy**
To make "the Aria never appears with a reason promising a price it doesn't have" a hard rule, code would have to check each reason against the catalogue before it is shown. Roughly:
- **Drop the reason:** the pick stays and its reason becomes `""`. This is the smallest change. The charter already says the UI must cope with an empty reason.
- **Drop the product:** the strip loses a product the model judged relevant.
- **Swap in a code-written reason:** for example, built from the catalogue figures.

Each of these makes code decide what a reason may say, which moves the charter's line. Detecting the contradictions is also its own problem. Spotting "under 100" or "top-rated" and comparing them with the data means parsing free text, and that check would miss phrasings it doesn't anticipate. I haven't done any of this.

If you want it, tell me which option you prefer and update the charter. Then I can implement it with a free local test over examples such as your Aria and USB-C cases. Separately, if you'd like to measure the prompt change first, I'd propose a small eval run and would agree a budget with you before any paid call.