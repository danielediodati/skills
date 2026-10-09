import unittest
from datetime import datetime

from seam import draft_reminder

APPOINTMENT = {
    "first_name": "Marta",
    "clinic": "Riverside Clinic",
    "when": datetime(2026, 10, 4, 9, 30),
    "prep": "no food for 8 hours before",
    "phone": "020 7946 0131",
}
GOOD = "Hi Marta, see you at Riverside Clinic on 4 Oct at 09:30. Please don't eat for 8 hours before."
TEMPLATE_TEXT = ("Hi Marta, a reminder of your appointment at Riverside Clinic "
                 "on 4 Oct at 09:30. Questions? Call 020 7946 0131.")


class FakeModel:
    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


def draft(answer, **options):
    return draft_reminder(APPOINTMENT, FakeModel(answer), **options)


class DraftReminderTest(unittest.TestCase):
    def test_good_message_is_sent_as_written(self):
        self.assertEqual(draft(GOOD), {"text": GOOD, "source": "model", "problem": None})

    def test_appointment_details_reach_the_model(self):
        model = FakeModel(GOOD)
        draft_reminder(APPOINTMENT, model)
        self.assertEqual(len(model.prompts), 1)
        for detail in ("Marta", "Riverside Clinic", "Date: 4 Oct", "Time: 09:30",
                       "no food for 8 hours before", "020 7946 0131", "160 characters"):
            self.assertIn(detail, model.prompts[0])

    def test_appointment_without_preparation(self):
        model = FakeModel(GOOD)
        draft_reminder({**APPOINTMENT, "prep": None}, model)
        self.assertIn("Preparation: none", model.prompts[0])

    def test_label_quotes_and_line_breaks_are_removed(self):
        result = draft('SMS: "Hi Marta,\n  see you on 4 Oct\nat 09:30."')
        self.assertEqual(result["text"], "Hi Marta, see you on 4 Oct at 09:30.")
        self.assertEqual(result["source"], "model")

    def test_too_long_message_is_replaced_by_the_template(self):
        result = draft(GOOD + " We look forward to seeing you!" * 3)
        self.assertEqual(result, {"text": TEMPLATE_TEXT, "source": "template", "problem": "too long"})

    def test_max_chars_can_be_lowered(self):
        result = draft(GOOD, max_chars=60)
        self.assertEqual(result["problem"], "too long")

    def test_empty_answer_is_replaced_by_the_template(self):
        result = draft("  \n ")
        self.assertEqual(result["text"], TEMPLATE_TEXT)
        self.assertEqual(result["problem"], "empty")

    def test_message_without_the_name_is_replaced(self):
        result = draft("Hello! Your appointment is on 4 Oct at 09:30.")
        self.assertEqual(result["problem"], "name missing")

    def test_message_without_the_date_is_replaced(self):
        result = draft("Hi Marta, see you tomorrow at 09:30.")
        self.assertEqual(result["source"], "template")
        self.assertEqual(result["problem"], "date missing")

    def test_message_with_another_day_is_replaced(self):
        result = draft("Hi Marta, see you on 14 Oct at 09:30.")
        self.assertEqual(result["problem"], "date missing")

    def test_month_written_in_full_is_accepted(self):
        result = draft("Hi Marta, see you on 4 October at 09:30.")
        self.assertEqual(result["source"], "model")

    def test_message_with_another_time_is_replaced(self):
        result = draft("Hi Marta, see you on 4 Oct at 19:30.")
        self.assertEqual(result["problem"], "time missing")


if __name__ == "__main__":
    unittest.main()
