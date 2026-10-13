I changed the summary prompt so the model is told to keep private details out of the summary. This lowers the chance of a leak but does not guarantee it. All 12 local tests pass, and nothing paid was run.

## What changed
- **`seam.py`**: the prompt now says the summary is shown in a list seen by many people, including outside the team, while the message is seen only by the handling agent. It names card numbers, security codes, passwords and other credentials, account or ID numbers, and health information, and asks the model to say what the customer needs, not the values they typed.
- **`test.py`**: a test checks that this instruction reaches the model.

The charter lists what the summary says as the model's decision, and criteria that inform the model's judgement don't move that line. The prompt supplies a criterion and leaves the wording to the model, so the charter is untouched.

## What this does not guarantee
- **The model can still slip.** A prompt lowers the rate of leaks but gives no guarantee, and the failure is silent. Because the leaks are card numbers, passwords and the like, you may want more than a lowered rate.
- **The fallback can leak.** If the model returns no usable summary, the code uses the stripped subject verbatim. A customer who puts their card number in the subject line would have it show up in the list. The charter fixes that fallback, so I left it.

## The line I did not move
A deterministic guarantee would need code that scrubs the summary or the fallback subject, for example patterns for card-like digit runs, CVC and password phrases. That would take over content the charter gives to the model, and it would only cover patterns someone anticipated. A redactor catches the card number but not "Tulip-Harbour-92". It would buy a hard floor on the worst cases, such as 13–19 digit runs, regardless of model behaviour. Whether to add it, and whether it may touch the subject fallback, is your decision and requires you to change the charter. I haven't touched it.

## Verifying the effect
I can't tell you from unit tests how often the model now leaks. Measuring that needs a paid eval run over cases like your two examples. If you want one, tell me a spending budget for the ticket and which model to use, and I'll start with the cheapest.