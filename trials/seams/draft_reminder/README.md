# draft_reminder

Used by a clinic's booking system to write the text message a patient receives before an appointment.

`draft_reminder(appointment, model, max_chars=160)` takes an appointment (`first_name`, `clinic`, `when` as a `datetime`, the clinic's `phone` and, optionally, `prep`: what the patient must do beforehand) and a model, any callable that takes a prompt string and returns a string. The model writes the message.

The function returns a dict with:

- `text`: the message to send
- `source`: `model` when the model's message is used, `template` when it was replaced by the clinic's fixed wording
- `problem`: why it was replaced (`empty`, `too long`, `name missing`, `date missing`, `time missing`), or `None`

The model's message is used only if it fits in `max_chars` and contains the patient's first name, the date (written like `4 Oct`) and the time (written like `09:30`) of the appointment.

Run the tests with `python -m unittest` from this directory.
