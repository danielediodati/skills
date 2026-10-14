Long tickets now reach the model with the customer's own words intact, so the 1,480 EUR ticket should route to billing. The 13 unit tests pass. I didn't call a real model, so the routing itself is unverified.

**What was wrong:** `triage_ticket` cut the body to its first 2000 characters before asking the model. A reply with three pages of quoted history above or below the customer's text meant the model never saw the request.

**What changed in `seam.py`:**
- **Quoted text is removed first.** Lines starting with `>`, lines ending in `wrote:`, and everything after an Outlook-style `-----Original Message-----` marker are dropped, wherever they appear in the message.
- **The limit is 4000 characters, and it keeps both ends.** If the remaining text is still too long, the model gets the first 2000 and the last 2000 characters, with a marker in between.

**Tests in `test.py`:**
- I replaced `test_only_the_start_of_a_long_body_is_sent`, which enforced the old behaviour, with `test_the_end_of_a_long_body_is_sent`.
- I added tests for a reply with quoted history below the new text, and for an Outlook original-message block.

I also added a short note on this to `README.md`.

**Limits to be aware of:**
- A request in the middle of a very long message, with no quoting to strip, can still be left out. Fixing that means sending the message in chunks and merging the results. I didn't do it because it changes cost and latency, and you may prefer to decide that.
- The heuristics assume English-style quote markers (`wrote:`). A reply header in another language, such as French "a écrit :", won't be stripped, and the quoted text will still reach the model. The `>` markers are language-neutral and still work.
- A customer's own line that ends in `wrote:` loses that one line. The rest of their text is kept.
- The folder is not a git repository, so I didn't commit anything.