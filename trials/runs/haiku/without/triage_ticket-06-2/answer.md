The ticket list summary no longer shows card numbers, security codes or passwords. Both of your examples now come out like this:

- `Wants the duplicate charge on card [card number] (CVC [code]) reversed.`
- `Can't log in with password [password] and wants access restored.`

The routing is unchanged, so the summary still says what the customer needs. All 17 tests pass with `python -m unittest`.

The change is in `seam.py`, in two layers:

- **Prompt:** the model is told never to repeat card numbers, security codes or passwords, and to say "a card" or "their password" instead.
- **Code:** a redaction step runs on every summary after the model answers. It removes 13–19 digit card numbers (with spaces or dashes), CVC/CVV/security codes next to their label, and the value after "password", "passcode", "passphrase" or "pin". The prompt is only a request, so the code step is what actually guarantees the list stays clean.

The fallback summary, which uses the raw subject when the model's answer is unusable, goes through the same redaction. Otherwise a card number in a subject line would have leaked through that path.

I added tests for both tickets, the subject fallback and the prompt wording. I also updated the README.

Things to be aware of:

- **Over-redaction:** any 13–19 digit run is treated as a card number, so a long order or reference number will also be masked. I chose this over a Luhn check, which would miss mistyped cards.
- **Password rule:** the value after "password" is removed unless the next word is a common one such as "reset", "link", "expired" or "not". I checked "password reset link never arrives" and "password is not working", and both stay readable.
- **Unhandled forms:** a password written without a label, such as "my login is Tulip-Harbour-92", is not caught. Neither is a card number written as words. Those would still depend on the prompt.
- **Existing tickets:** summaries that were already stored are not changed. If the old summaries are still visible in the list or the weekly report, they will need a separate cleanup.