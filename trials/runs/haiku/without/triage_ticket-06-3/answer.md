The summary now keeps the customer's need and drops the card number, security code, and password. Both of your examples come out like this:

- `Wants the duplicate charge on card 4539 1488 0343 6467 (CVC 318) reversed.` → `Wants the duplicate charge on card [card number] (CVC [code]) reversed.`
- `Can't log in with password Tulip-Harbour-92 and wants access restored` → `Can't log in with password [secret] and wants access restored`

All 16 tests pass with `python -m unittest`, including five new ones for these cases.

**What changed in `seam.py`**
- **Prompt:** asks the model not to repeat card numbers, security codes, passwords, PINs or other secrets, and to say "a card" or "the password" instead.
- **Redaction after the model:** the model's summary goes through a fixed set of patterns before it is returned. This is the actual guarantee, because a prompt instruction alone won't reliably stop a model from repeating a number.
  - Card numbers: 13 to 19 digits, with or without spaces or dashes.
  - Security codes after a label: CVC, CVV, CSC, CID, "security code".
  - Passwords, passcodes, passphrases and PINs, with the value that follows them.
- **Fallback:** when the model's answer is unusable, the summary falls back to the subject, and that is redacted too. Customers can type secrets into subjects as well.
- **Length cap:** the cap is applied after redaction, so a card number can't be cut partway and leave digits showing.

**Choices you may want to change**
- Card numbers are redacted on digit count alone, without a Luhn check. This over-redacts order or reference numbers of that length, which I think is the right trade-off here.
- Common words after "password" are left alone ("password reset", "password is expired", "password not working"). The list is in `SECRET_PATTERNS` if your support vocabulary differs.
- I updated `README.md` to describe the redaction.

**Not covered:** the full ticket body is still sent to the model for routing, and the agent still sees it unredacted in the ticket. You asked about the list, so I left that alone. If the model provider is outside your data-protection boundary, that is a separate question worth raising.