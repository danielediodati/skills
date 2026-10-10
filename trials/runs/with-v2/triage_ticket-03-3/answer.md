Summaries over 120 characters no longer end mid-word, and a shortened summary now ends with `…`. All 15 tests pass.

The change is in `seam.py`, in a new `_fit` function that replaces the plain `[:120]` cut:

- **Fits:** a summary of 120 characters or fewer is returned unchanged.
- **Several sentences:** the leading sentences that fit are kept whole, followed by ` …`.
- **No sentence fits:** the text is cut at the last word boundary, trailing punctuation is dropped, and `…` is appended. A single word with no spaces is hard-cut and still marked.

The result is never longer than 120 characters, so the list column is unchanged. The subject fallback goes through the same function.

Your first example now reads "The customer would like to keep the subscription for the three seats used by the design team but wants to cancel the…".

This stays within the charter: the model still writes the summary freely, and code only constrains how it is shortened. I did not touch the charter or the prompt.

I updated the existing cap test, which expected a hard cut at 120, and added tests for each case above. The README also notes the new behaviour.

One thing I left alone: the charter says an invalid queue or urgency should be `null`, "not yet in code, which puts `general` and `normal`". That is a separate gap from this request.