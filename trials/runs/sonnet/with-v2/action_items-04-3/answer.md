Tasks now keep their owner when the notes name someone who was in the meeting, including by first name or nickname. The 18 tests pass, but I have not run the change against a real model. The tests use a fake model.

**Cause:** the prompt told the model to write the owner "as written in the list above". The code then kept an owner only on an exact full-name match. When the notes said "Tom" and the model answered "Tom", the code treated that as not an attendee and set the owner to `None`. That is what happened to your venue and badges items.

**Changes in `seam.py`:**
- **Prompt:** the model is told that notes often use a first name or a nickname ("Tom", "Tommy", "Ana R."). When that is one of the people present, it should write their full name exactly as in the attendee list. It writes "none" if the notes don't make clear who took the task.
- **Code:** the owner is no longer thrown away because it isn't an exact attendee name. An attendee match (ignoring case and spacing) is returned in the caller's spelling, and any other name is kept as the model wrote it.

I also updated the README and the owner test. The test used to assert that an owner who was not at the meeting is dropped; it now asserts the name is kept.

Resolving "Tom" to Tom Becker is the model's decision, so it depends on the model following the new prompt wording. The code does not guess names itself.

Two other places where the code and charter disagree, which you didn't ask about, so I left them alone:
- Due dates that code rejects still come out as `None`, indistinguishable from a date never given.
- The list is still capped at 10 items.