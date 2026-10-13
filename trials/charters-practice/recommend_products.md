# recommend_products charter

Input: the shopper's search text, the catalogue (id, name, price, rating, in_stock), a model callable, and a limit (default 5).
Output: a list of at most `limit` in-stock catalogue products, best first, each with id, name, price, rating (from the catalogue) and a one-line reason of at most 80 characters.

## Free
- Which products suit the search: relevance is a judgment about meaning, with no rule code can state. The model may also pick fewer than `limit`, or none, when little fits.
- The order of the picks: ranking by fit is the same judgment; code keeps the model's order and never re-sorts by rating or price.
- The wording and angle of each reason: persuasive prose addressed to the customer is language work. Nothing checks it against the catalogue, so it may claim things the model was never given. Assumed.

## Constrained
- Which products are offered to the model: code sends only in-stock products, so out-of-stock items cannot be picked and tokens are not spent on them.
- Whether a pick is real: the ID must match an offered in-stock product exactly (after stripping whitespace), otherwise it is dropped; the model may not invent products, and case or format variants are dropped, not repaired.
- Whether a pick is in stock: checked in code as well, as a pick can only be accepted if it was offered.
- Each product once: the first mention wins, repeats are ignored.
- Product name, price and rating: always read from the catalogue, never from the model's text, so a shown fact cannot be wrong.
- Maximum count: code stops at `limit`, whatever the prompt asked.
- Fewer valid picks than asked: the shorter list is returned as is. Code never backfills with unpicked products, as that would show products no one judged to fit.
- Reason length and shape: whitespace collapsed to one line and cut at 80 characters, because the UI slot is fixed. The cut is mid-word, with no ellipsis.
- A pick with no reason: kept, with an empty reason, because the pick is the value and the reason is decoration.
- Answer format: code parses `ID | reason` lines and ignores list markers and chatter, so format noise does not lose picks.
- Query cleanup: whitespace is normalised in code; a blank query returns an empty list without calling the model, as no judgment is possible.
- Nothing in stock: returns an empty list without calling the model, as the answer is known.
- Invalid `limit` (below 1): refused with ValueError, a caller bug that must not be hidden.
- Failure policy: an unusable answer gives an empty list, and an exception from the model propagates. Code does not retry or fall back to a rating-sorted list, so the page decides what to show.

## Target and budget
- Budget: one model call per search, no retries.
- Candidate set: code bounds how many products reach the model, as the prompt must fit its context and cost grows with the catalogue. Not yet in code, which sends every in-stock product with no cap.
