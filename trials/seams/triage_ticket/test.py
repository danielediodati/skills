import unittest

from seam import triage_ticket


class FakeModel:
    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


TICKET = {
    "subject": "Charged twice",
    "body": "I was charged twice for my September invoice.",
    "tier": "pro",
}


def triage(answer, **changes):
    return triage_ticket({**TICKET, **changes}, FakeModel(answer))


class TriageTicketTest(unittest.TestCase):
    def test_valid_answer_is_used(self):
        result = triage(
            "queue: billing\nurgency: high\nsummary: Wants a duplicate charge refunded."
        )
        self.assertEqual(result, {
            "queue": "billing",
            "urgency": "high",
            "summary": "Wants a duplicate charge refunded.",
            "respond_within_hours": 8,
        })

    def test_ticket_text_reaches_the_model(self):
        model = FakeModel("queue: billing\nurgency: low\nsummary: x")
        triage_ticket(TICKET, model)
        self.assertEqual(len(model.prompts), 1)
        self.assertIn("Charged twice", model.prompts[0])
        self.assertIn("September invoice", model.prompts[0])

    def test_decorated_answer_is_understood(self):
        result = triage("**Queue:** Billing.\n- URGENCY: `Low`\nSummary: Refund.")
        self.assertEqual(result["queue"], "billing")
        self.assertEqual(result["urgency"], "low")
        self.assertEqual(result["summary"], "Refund.")

    def test_unknown_queue_goes_to_general(self):
        result = triage("queue: refunds\nurgency: high\nsummary: x")
        self.assertEqual(result["queue"], "general")

    def test_unknown_urgency_is_normal(self):
        result = triage("queue: billing\nurgency: asap\nsummary: x")
        self.assertEqual(result["urgency"], "normal")
        self.assertEqual(result["respond_within_hours"], 24)

    def test_unusable_answer_falls_back_everywhere(self):
        result = triage("I am not sure what this ticket is about.")
        self.assertEqual(result, {
            "queue": "general",
            "urgency": "normal",
            "summary": "Charged twice",
            "respond_within_hours": 24,
        })

    def test_enterprise_is_raised_one_level(self):
        result = triage("queue: billing\nurgency: normal\nsummary: x", tier="enterprise")
        self.assertEqual(result["urgency"], "high")
        self.assertEqual(result["respond_within_hours"], 8)

    def test_enterprise_urgent_stays_urgent(self):
        result = triage("queue: billing\nurgency: urgent\nsummary: x", tier="enterprise")
        self.assertEqual(result["urgency"], "urgent")
        self.assertEqual(result["respond_within_hours"], 1)

    def test_summary_is_one_line_and_capped(self):
        result = triage("queue: billing\nurgency: low\nsummary:  a   b " + "c" * 200)
        self.assertTrue(result["summary"].startswith("a b ccc"))
        self.assertEqual(len(result["summary"]), 120)

    def test_only_the_start_of_a_long_body_is_sent(self):
        model = FakeModel("queue: general\nurgency: low\nsummary: x")
        triage_ticket({"subject": "Hi", "body": "x" * 2000 + "TAIL"}, model)
        self.assertNotIn("TAIL", model.prompts[0])

    def test_empty_ticket_is_refused_before_asking_the_model(self):
        model = FakeModel("queue: general\nurgency: low\nsummary: x")
        with self.assertRaises(ValueError):
            triage_ticket({"subject": " ", "body": ""}, model)
        self.assertEqual(model.prompts, [])


if __name__ == "__main__":
    unittest.main()
