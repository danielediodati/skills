Summaries no longer show card numbers, security codes, or passwords. The first ticket would now read "Wants the duplicate charge on card [redacted] (CVC [redacted]) reversed.", and the login ticket reads "Can't log in with password [redacted] and wants access restored." All 18 tests pass, including new ones for both cases.

Changes in `seam.py`:

- **Prompt:** the model is told to leave out card numbers, security codes and passwords, and to write "the card" or "the password" instead.
- **Code-side redaction:** the model's summary is always passed through `_redact` before the 120-character cap, so a model that ignores the prompt still can't leak the value. The subject fallback goes through it too, since a subject can carry the same details.
- **What gets redacted:** any run of 13–19 digits, with optional spaces or dashes; a CVC/CVV/security code next to its label; and the value after "password", "passcode", "passwd" or "pwd", including "password is X".

I also added tests in `test.py` for each case and checked that ordinary numbers such as "Order 10482" and dates are kept.

Limits to know about:

- **Multi-word passwords:** only the first word after the label is redacted, so "password Tulip Harbour 92" leaves "Harbour 92" showing.
- **Over-redaction:** "forgot my password and need help" becomes "forgot my password [redacted] need help". I accepted that because leaking is worse than a clumsy summary.
- **Other secrets:** bank account numbers, IBANs and national ID numbers are not covered. Say if you want them added.
- **Existing data:** this only affects summaries generated from now on. Tickets already in the list or in past weekly reports are not fixed.

The full ticket body, card number included, is still sent to whichever model `triage_ticket` calls. Redacting the summary does not change that. If that model is an external service, it's worth deciding separately whether the body should be redacted before the call.

This folder is not a git repository, so I didn't commit anything.