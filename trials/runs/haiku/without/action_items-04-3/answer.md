Owners now resolve from the names your notes use. For your 3 March example, the list comes back as Ana Ruiz on the quote (due 6 March), Tom Becker on the venue, and Priya Raman on the badges. I ran that example through the code with a stand-in for the model, not a real model, so the model's own output is still untested.

The fix is in `seam.py`. A name in the answer now matches an attendee if it is:
- the full name, in any case or spacing (as before);
- a first name, or a nickname that shortens it, such as "Tommy" or "Tom" for "Tom Becker";
- a surname, such as "Becker";
- a first name with an initial, such as "Ana R.".

If the name fits more than one attendee, the owner stays empty rather than guessing. Someone who wasn't at the meeting still comes back unowned, and the item is kept.

I also loosened the prompt so the model can copy names as the notes write them, and updated the owner rule in `README.md`. `test.py` has 6 new tests covering these cases, and all 23 pass.

Limits:
- A nickname has to shorten the first name. "Tommy" works for "Tom", but "Bob" for "Robert" or "Liz" for "Elizabeth" won't match. Covering those needs an alias list from the caller, which I haven't added.
- This isn't a git repository, so I haven't committed anything.