I changed the prompt in `seam.py` so the model is told to write an attendee's full name from the list when the notes use a first name or nickname. The 18 unit tests pass, but they use a fake model, so I haven't seen a real model produce "Tom Becker" for your example.

**Likely cause.** The prompt only said "as written in the list above". A model reading "Tom looks into the venue" can reasonably answer `Tom`. The code then keeps an owner only if it exactly matches an attendee (ignoring case and spacing), so "Tom" became `None`.

**What the prompt now says.**
- Notes usually use first names or nicknames ("Tom", "Tommy", "Ana R."). When one clearly means a person present, the model writes that person's full name from the list.
- A person who isn't in the list, or a name that could mean more than one attendee, is "none".

I also added a test asserting that the prompt carries this instruction.

**What I left alone.** The charter keeps owner matching strict on purpose: code never guesses a closer match, so a task is never given to someone who wasn't named. I didn't add first-name or fuzzy matching in code, because that would move that line.

**Remaining risk.** A model that still answers "Tom" will still lose the owner, and the item stays unowned rather than guessed. Try your 3 March notes against your real model. If owners still drop, the options are changing the charter to allow code-side matching, or giving the model the invitation names alongside the nicknames. Both are your call.