I haven't changed anything. Every fix for this moves a line the charter holds, and only you can move those.

**What happens now**

The model's answer is parsed as `ID | reason`. When the model gives only the ID, or `ID |` with nothing after it, the pick is kept with `reason: ""`. That is what happened to the Pico earbuds and the 2 m cable. The code isn't dropping text. The model never wrote a reason for those two.

**Why I can't fix it without moving a line**

`evals/recommend_products/charter.md` rules out each way of getting a reason onto every card:

| Fix | Charter line it moves |
|---|---|
| Drop picks that have no reason | "A pick with no reason is kept with `""`, not dropped: the product is valid even if its explanation is missing." |
| Retry the call, or ask again for the missing reasons | "no retry or fallback ranking"; budget is "one model call per request … No retries." |
| Fill the gap in code with a stock line such as "Also matches your search" | Reason wording is Free ("in the model's own words"). A canned reason takes that decision over. |
| Reword the prompt to demand a reason on every line | "Prompt shape is fixed: … the instruction wording and answer format." |

**What each move would buy**

- **Dropping reasonless picks:** this is the smallest change and costs no extra calls. No card is ever blank, but the strip gets shorter. In your example it would have shown only the Aria headphones. It also removes the products you said needed explaining.
- **Adding a second model call for only the missing reasons:** the strip stays full and every reason is written for the shopper. It costs an extra call on some requests and breaks the one-call budget.
- **Rewording the prompt:** this is cheapest and keeps the model in charge of the wording. It makes blanks less likely but doesn't guarantee none. Dropping or retrying would still be needed if you want a guarantee.
- **A fixed fallback line in code:** this is guaranteed and free, but it is exactly the generic text that makes the strip look like a second results list.

**What I need from you**

Pick one, or tell me which charter line to relax:

1. Drop reasonless picks.
2. Retry once for the missing reasons.
3. Strengthen the prompt wording.
4. Use a code-side fallback line.

Option 3 is my recommendation, ideally paired with option 1 as the guarantee. Together they keep the wording with the model and never show a blank card. The cost is that you may see fewer than three cards on a bad answer.

Whichever you choose, I'll update the tests: `test_pick_without_a_reason_has_an_empty_one` currently asserts the behaviour you're reporting. Any real-model verification would be a paid run, so I'd agree a budget with you before making it.