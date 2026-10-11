Tasks now keep their owner when the notes use a first name, a nickname or an initial. In your example, "Look into the venue" goes to Tom Becker and "Order the badges" to Priya Raman. All 19 tests pass, including the new ones.

**Cause:** the tool only accepted an owner if it matched an attendee's full name exactly. When the model wrote "Tom" or "Priya", the lookup missed and the owner was silently set to none. The task and date were kept, which is why only the owner went missing.

**Changes in `seam.py`:**
- **Prompt:** the model is now told that notes may use first names, nicknames or initials, and to answer with the attendee's full name from the list. It should write "none" only if it's unclear who took the task.
- **Matching:** the model's answer is now matched leniently against the attendees, as a safety net. The new `_match_attendee` accepts:
  - a first or last name alone ("Tom", "Raman");
  - a short or longer form of a name that starts the same way ("Tommy" for Tom);
  - an initial ("Ana R.").
- **Ambiguity:** if more than one attendee fits (two Anas, say), the owner stays empty rather than guessing wrong. Names of people who weren't in the meeting are still dropped.

**Limits:**
- The code can't know unrelated nicknames like "Bill" for William. Those depend on the model's mapping through the new prompt wording.
- It also won't resolve a lone initial such as "A.".

The new tests are in `test.py`: resolved names, plus ambiguous and unknown names left unowned.