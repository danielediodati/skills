import unittest
from datetime import date

from seam import MAX_ITEMS, MAX_TASK_CHARS, ActionItem, extract_action_items

ATTENDEES = ["Ana Ruiz", "Tom Becker", "Priya Raman"]
MEETING = date(2026, 3, 3)  # a Tuesday
NOTES = "Ana will send the quote to Halden by the 6th. Tom looks into the venue."


class FakeModel:
    """Returns a canned answer and remembers the prompts it was given."""

    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


def run(answer, notes=NOTES):
    return extract_action_items(notes, ATTENDEES, MEETING, FakeModel(answer))


class PromptTest(unittest.TestCase):
    def test_model_is_asked_once_with_notes_attendees_and_date(self):
        model = FakeModel("NONE")
        extract_action_items(NOTES, ATTENDEES, MEETING, model)
        self.assertEqual(len(model.prompts), 1)
        prompt = model.prompts[0]
        self.assertIn(NOTES, prompt)
        self.assertIn("Ana Ruiz, Tom Becker, Priya Raman", prompt)
        self.assertIn("2026-03-03", prompt)

    def test_blank_notes_do_not_reach_the_model(self):
        model = FakeModel("Do something | Ana Ruiz | none")
        self.assertEqual(extract_action_items("  \n", ATTENDEES, MEETING, model), [])
        self.assertEqual(model.prompts, [])


class ParsingTest(unittest.TestCase):
    def test_well_formed_lines_become_items(self):
        items = run(
            "Send the quote to Halden | Ana Ruiz | 2026-03-06\n"
            "Look into the venue | Tom Becker | none\n"
        )
        self.assertEqual(
            items,
            [
                ActionItem("Send the quote to Halden", "Ana Ruiz", date(2026, 3, 6)),
                ActionItem("Look into the venue", "Tom Becker", None),
            ],
        )

    def test_none_answer_gives_no_items(self):
        self.assertEqual(run("NONE"), [])

    def test_chatter_header_and_malformed_lines_are_skipped(self):
        items = run(
            "Here are the action items:\n"
            "task | owner | due\n"
            "Book the room | Tom Becker\n"
            " | Ana Ruiz | 2026-03-06\n"
            "Order the badges | Priya Raman | 2026-03-10\n"
        )
        self.assertEqual(
            items, [ActionItem("Order the badges", "Priya Raman", date(2026, 3, 10))]
        )

    def test_bullets_numbering_and_stray_spacing_are_tolerated(self):
        items = run(
            "1. Book the room |Tom Becker|2026-03-05\n"
            '- "Order   the badges." |  Priya Raman | 2026-03-10\n'
        )
        self.assertEqual(
            [item.task for item in items], ["Book the room", "Order the badges"]
        )

    def test_task_may_contain_a_pipe(self):
        items = run("Rename the A|B test report | Ana Ruiz | none")
        self.assertEqual(items[0].task, "Rename the A|B test report")
        self.assertEqual(items[0].owner, "Ana Ruiz")


class OwnerTest(unittest.TestCase):
    def test_owner_is_returned_as_the_caller_spelled_it(self):
        items = run("Book the room | tom  BECKER | none")
        self.assertEqual(items[0].owner, "Tom Becker")

    def test_owner_who_was_not_in_the_meeting_is_dropped_but_item_kept(self):
        items = run("Approve the budget | Marta Olsen | none")
        self.assertEqual(items, [ActionItem("Approve the budget", None, None)])

    def test_explicit_none_owner(self):
        self.assertIsNone(run("Find a caterer | none | none")[0].owner)


class DueTest(unittest.TestCase):
    def test_unreadable_or_impossible_date_becomes_none(self):
        items = run(
            "Book the room | Tom Becker | soon\n"
            "Order the badges | Priya Raman | 2026-02-30\n"
        )
        self.assertEqual([item.due for item in items], [None, None])

    def test_date_before_the_meeting_becomes_none(self):
        self.assertIsNone(run("Book the room | Tom Becker | 2026-03-02")[0].due)

    def test_date_on_the_meeting_day_is_kept(self):
        self.assertEqual(run("Book the room | Tom Becker | 2026-03-03")[0].due, MEETING)


class ListTest(unittest.TestCase):
    def test_sorted_by_deadline_with_undated_items_last_in_original_order(self):
        items = run(
            "First undated | Ana Ruiz | none\n"
            "Later | Tom Becker | 2026-03-20\n"
            "Second undated | Ana Ruiz | none\n"
            "Sooner | Priya Raman | 2026-03-05\n"
        )
        self.assertEqual(
            [item.task for item in items],
            ["Sooner", "Later", "First undated", "Second undated"],
        )

    def test_same_task_and_owner_is_listed_once(self):
        items = run(
            "Book the room | Tom Becker | 2026-03-05\n"
            "book the room. | Tom Becker | none\n"
            "Book the room | Ana Ruiz | none\n"
        )
        self.assertEqual(
            [(item.owner, item.due) for item in items],
            [("Tom Becker", date(2026, 3, 5)), ("Ana Ruiz", None)],
        )

    def test_list_is_capped_keeping_the_soonest_deadlines(self):
        lines = [f"Task {n} | Ana Ruiz | none" for n in range(MAX_ITEMS)]
        lines.append("Urgent task | Tom Becker | 2026-03-04")
        items = run("\n".join(lines))
        self.assertEqual(len(items), MAX_ITEMS)
        self.assertEqual(items[0].task, "Urgent task")

    def test_long_task_is_cut_at_a_word_boundary(self):
        task = "Write up " + "the findings and " * 12 + "share them"
        cut = run(f"{task} | Ana Ruiz | none")[0].task
        self.assertLessEqual(len(cut), MAX_TASK_CHARS)
        self.assertTrue(cut.endswith("…"))
        self.assertTrue(task.startswith(cut[:-1] + " "))


if __name__ == "__main__":
    unittest.main()
