I changed the prompt in `seam.py` so the model is told it may recommend nothing, and the local tests pass (15 of 15). I have not checked how a real model behaves on "kettle", because that needs paid calls.

**Cause:** the prompt said "Pick up to N products that best match", which never allowed an empty answer. The model filled the strip with the least-bad products and wrote a generic reason for each.

**Change:**
- **Prompt:** it now says to pick a product only if it genuinely suits the search, and to answer with an empty reply if nothing does, since showing nothing beats showing something unrelated.
- **Code:** unchanged. An empty or chatter-only answer already becomes `[]`, with no fallback fill by rating or price.
- **Tests:** two new ones cover the prompt wording and the empty-answer case.

**Decision for you:** I deliberately did not add a relevance filter in code. Relevance and how many to return are the model's decisions under the charter, and a code check would take that over. The catch is that the prompt makes "nothing" possible but cannot guarantee it. If a model still pads the strip, we need a real-model check.

**Next step, if you want it:** a small paid check of a few searches ("kettle", a misspelling, a brand we don't carry, plus "headphones" as a control) against the real model. It would be a handful of single-call requests. Tell me which model and a spending budget for the ticket, and I'll run it.

I haven't touched the charter. Its Free section already covers "none up to `limit`".