I changed the summary so it no longer carries card numbers, security codes or passwords, but I couldn't run the tests, so the change is unverified. The shell command I used to run them was blocked, so I made the edits with the file tools and checked the new tests by reading through them only. Please run `python -m unittest` before relying on it.

## What changed (`seam.py`)

There are three layers, because the model alone can't be trusted to leave things out:

1. **Prompt instruction.** The model is told the summary is shown to every agent and in external reports, and to say what *kind* of thing it is ("a duplicate card charge", "a password") rather than quoting it.
2. **Secrets removed before the model sees the ticket.** Subject and body are scrubbed first, so the model can't repeat what it never received. Your first example would reach it as `card [card number] (CVC [removed])`, which is still enough to route.
3. **Scrub on the way out.** Whatever the model returns, and the subject fallback used when the model's answer is unusable, goes through the same scrubber. A password found in the body is also removed from the summary wherever it appears, even without the word "password" next to it.

### What the scrubber catches
- **Card numbers:** 13–19 digits, optionally grouped with spaces or hyphens, become `[card number]`.
- **Security codes:** `CVC`, `CVV`, `CID` or "security code" followed by 3–4 digits.
- **Passwords:** `password`, `passcode`, `passphrase`, `pwd` or `PIN`, followed by a quoted value, a value after `is`, `:` or `=`, or a bare token containing a digit or symbol (`password Tulip-Harbour-92`). "password reset" and "password isn't working" are left alone.

## Limits
- **Passwords can't be reliably detected from free text.** The scrubber depends on the customer writing the word "password" (or similar) next to it. A bare "I tried sunshine99 and it failed" would get through if the model repeated it.
- **Other personal details aren't redacted.** Account numbers, addresses, phone numbers and national IDs are only covered by the prompt instruction, which is the weakest layer. If you want them enforced in code too, send me the formats you see.
- **Over-redaction is possible.** Any 13–19 digit run is treated as a card number, so a long order or tracking number will be replaced. I chose that over missing a real card.
- **The ticket body itself is unchanged.** Redacting it for the agent who opens it is still your existing manual process.
- **Existing summaries aren't touched.** Ones already stored, and ones already sent in weekly reports, still contain whatever they contained.

## Tests (`test.py`)
I added six tests: your card/CVC example, your password example, a password stated in the body and repeated by the model, secrets not appearing in the prompt, the subject fallback, and ordinary "password reset" text staying untouched.