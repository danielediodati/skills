Summaries no longer carry card numbers, security codes or passwords. All 16 tests pass, 5 of them new.

**What changed (`seam.py`)**
- **Redaction before the model:** the subject and body are redacted before they go to the model, so it never sees the secrets and can't repeat them. This happens before the 2000-character cut, so a card number can't be split and slip through.
- **Redaction after the model:** the model's summary is redacted again, as is the subject used as a fallback when the model gives nothing usable.
- **Prompt instruction:** the model is told to say what kind of detail was given, not the detail itself.
- **What gets redacted:**
  - Digit runs of 13–19 digits, with spaces or dashes, become `[card number removed]`.
  - `CVC`, `CVV` and `security code` followed by 3–4 digits become `CVC [removed]` (or the matching label).
  - `password`, `passcode`, `passphrase` and `PIN` followed by a value become `password [removed]`.
- **Plain mentions stay readable:** "Forgot password and cannot log in" is untouched. A bare value with no `is`, `:`, `=` or quotes is masked only if it contains a digit or symbol.

Your two examples now read:
- "Wants the duplicate charge on card [card number removed] (CVC [removed]) reversed."
- "Can't log in with password [removed] and wants access restored"

**Limits**
- **Pattern-based:** a password written as a plain word with no cue, such as "I typed Tulip", will get through. The same goes for a password in a word-only phrase like "password is correct horse".
- **Order numbers:** any run of 13 or more digits is treated as a card, so a long order or tracking number will be masked too. I chose over-masking over leaks.
- **Other secrets:** IBANs, API keys, national ID numbers and similar are not covered. Tell me if you want any added.
- **Raw ticket and model call:** the ticket body is not changed, so agents still see the original and can redact it there as you do now. The redacted text is also what goes to whatever model you pass in.
- **Existing summaries:** this only affects new tickets. Summaries already in the list or in past weekly reports aren't touched.

Changes are in `seam.py`, `test.py` and `README.md`.