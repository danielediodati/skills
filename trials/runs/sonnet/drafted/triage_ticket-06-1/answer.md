I changed the prompt so the model is told not to repeat private details in the summary. This reduces the leak but does not guarantee it.

**What changed**
- `seam.py`: the prompt now says the summary is shown in a widely seen list and in reports. It asks the model to say what the customer needs without repeating card numbers, security codes, passwords or other credentials, or account and personal identifiers.
- `test.py`: one new test checks that the instruction reaches the model.
- The 12 local tests pass. Nothing paid was run, and I did not touch the charter.

**What this does not guarantee**
- The charter lists the summary's wording as the model's decision, and says code "never checks its content". A prompt instruction is a criterion the model weighs, so it fits within that. The model can still slip, and nothing in code would catch it.
- I did not measure how often it slips. That would take a paid eval run on tickets containing card numbers, passwords and similar details. I'd agree a budget with you before running one.

**Two gaps**
- **Subject fallback:** if the model returns no summary, code falls back to the ticket subject. A customer who puts a card number in the subject would still see it in the list.
- **No code-side guarantee:** a guarantee would need code to scan or redact the summary, for example for card-number patterns. That checks the summary's content in code, which the charter says it doesn't do, so I stopped there. Doing it would give a hard guarantee for the patterns it recognises (card numbers, for instance). It would not cover free-form secrets like `Tulip-Harbour-92`.

If you want a guarantee, that charter change is yours to make. Tell me if you want one, and I can write the check once the charter allows it.