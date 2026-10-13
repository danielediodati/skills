I changed the prompt so the model is told to give the full attendee name, but I haven't confirmed it fixes your example. That needs a paid model run.

## What I think was happening

The code only keeps an owner whose text matches an attendee's full name from the invitation, ignoring case and spacing. If the model answers `Tom` or `Priya` for "Tom looks into the venue", the owner is dropped to `None` and the task is kept. That fits your symptom, but I haven't seen the model's actual answers.

## What I changed

- **`seam.py`:** the `owner` instruction in the prompt now says to write the full name exactly as in the attendee list. It also says notes will use first names, nicknames or initials ("Tom", "Tommy", "Ana R."), and the model must map those to the matching full name. It should answer "none" when the notes don't make clear which attendee took the task.
- **`test.py`:** one new test checks that the prompt carries this instruction. All 18 tests pass.

## What I did not change

The charter's rule that an owner must match an attendee exactly is a constrained line: "a first name only, a variant spelling becomes `None`". A prompt change cannot override it. If the model still returns "Tom" or "Tommy" some of the time, those owners will keep disappearing.

The fix for that would be to loosen the match in code, for example to accept an unambiguous first name or a nickname. That would buy you the owners in your example even when the model slips. The cost is that code would start guessing who a short name refers to, which the charter currently rules out. That is your decision, and I haven't touched the charter or the matcher.

## Next step

To confirm the prompt change works, I'd run your 3 March example through the real model. That is a paid call, so tell me which model to use and a spending budget for this ticket, and I'll run it.