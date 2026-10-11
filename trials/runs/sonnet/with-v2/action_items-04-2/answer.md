The owners were being lost in two places. I've fixed both, but I haven't run the change against a real model, so the 3 March example is unconfirmed.

**What was going wrong**
- The prompt asked the model for the owner's name "as written in the list above". With notes saying "Tom looks into the venue", the model most likely wrote `Tom`.
- The code then kept an owner only if it matched an attendee's full name exactly (`Tom Becker`). Anything else, such as `Tom`, `Tommy` or `Ana R.`, was silently turned into no owner.

**What I changed**
- **`seam.py` prompt:** the model is now told that notes often use first names, nicknames or initials, and that when the person is one of those present it should write their full name exactly as in the attendee list. Someone who wasn't present is written as the notes give them. "none" is only for items nobody took.
- **`seam.py` code:** an owner matching an attendee is still returned spelled as you gave it. Any other owner text is now kept as the model wrote it instead of being dropped, so an unresolved "Tommy" still shows up as an owner rather than a blank.
- **`test.py` and `README.md`:**
  - The old test that dropped non-attendee owners now asserts they are kept.
  - A new test checks the prompt asks for full names for first names and nicknames.
  - The README's owner bullet is updated to match.
- **Tests:** all 18 pass.

**Limits**
- **Model-dependent:** whether "Tommy" becomes `Tom Becker` depends on the model following the new prompt. The matching is not done in code, because who an owner is stays the model's call under the charter.
- **Charter untouched:** the charter already listed owner as free text and noted the code didn't yet match, so this brings the code in line with it. I didn't edit the charter.