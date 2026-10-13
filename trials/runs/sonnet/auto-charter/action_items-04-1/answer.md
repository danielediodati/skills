I changed the prompt so the model is asked to name the owner in full, but this does not guarantee the owners come out filled in. The tests pass (18, including a new one for the prompt wording), but I haven't run it against a real model, so I can't say whether "Tom looks into the venue" now comes back as Tom Becker.

**Cause:** the model was probably answering "Tom" or "Priya" as the owner. The code (`seam.py`) keeps an owner only if it matches an attendee's full name as written in the list, so a first name or nickname was turned into no owner and the task kept.

**Change:** the prompt's `owner` instruction now:
- asks for the full name exactly as in the attendee list;
- says the notes may use first names, nicknames ("Tommy", "Ana R.") or "I";
- asks the model to work out which person present is meant;
- keeps "none" for when nobody took it or it can't tell who.

This only gives the model more to go on. It still decides who owns each task, and the answer is still checked against the attendee list.

**What I did not change:** the charter (`evals/action_items/charter.md`) says the code never guesses a closer match, so a task is never assigned to someone who wasn't named. Matching "Tom" to "Tom Becker" in code would make this reliable, but it moves that line, and only you can decide to do that.

If owners still go missing, here is what that would buy and cost:
- **Gain:** a first name or nickname the model passes through would still land on the right person, which is the guarantee you're after.
- **Cost:** a wrong match becomes possible. For example, with two attendees named Tom, code would have to either refuse or guess.

Tell me if you want to revise the charter that way, and I'd then implement it.