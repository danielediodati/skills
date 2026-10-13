Summaries are now redacted in `seam.py`, so both of your examples would come out clean. All 18 tests pass, including 7 new ones.

For example, the first ticket now reads "Wants the duplicate charge on card [removed] (CVC [removed]) reversed." The second reads "Can't log in with password [removed] and wants access restored."

**What I changed**
- **Before the model:** the subject and body are redacted before they reach the model, so it never sees a card number or password it could repeat.
- **In the prompt:** it now tells the model not to copy credentials into the summary.
- **After the model:** the returned summary, including the subject fallback, is redacted again. This is the guarantee that doesn't depend on the model behaving. It runs before the 120-character cut, so a truncated summary can't leave half a secret behind.

**What gets redacted**
- Card numbers: 13–19 digits, with or without spaces or dashes. I deliberately skipped the Luhn check, since customers mistype numbers.
- Codes: CVC, CVV, CSC, "security code" or PIN followed by digits.
- Passwords: "password", "passcode", "passphrase" or "pwd" followed by a value, including `password: x`, `password is x` and quoted values.
- Ordinary phrasing such as "password reset" or "forgot password and…" is left alone via a small stoplist.

**Limits**
- Redaction is pattern based. A password given with no cue word ("I typed Tulip-Harbour-92 and it failed") will not be caught.
- A bare word after "password" that isn't on the stoplist is treated as a password and removed, so you may occasionally see `[removed]` where a harmless word stood.
- Other sensitive data (bank account numbers, API keys, addresses) is not covered.
- Summaries already stored or emailed from before this change are untouched.

Passing the ticket text through a dedicated PII detection step would be the sturdier long-term option. Until then, `redact_secrets` is the one place to add patterns.