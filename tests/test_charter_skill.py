"""The `charter` skill and the brief a trial gives its writing agent are one text.

    uv run --no-project python -m unittest discover -s tests

The trials measure the charter an agent writes from `trials/brief-auto-charter.md`; the plugin ships
the `charter` skill. What a charter is, how to write it and its format are the same words in both,
so a number measured on one holds for the other.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "a4a" / "skills" / "charter" / "SKILL.md"
BRIEF = REPO / "trials" / "brief-auto-charter.md"
FIRST_HEADING = "## What a charter is\n"
FENCE = "```\n"


def shared_text(brief: str) -> str:
    """From the brief's first section to the end of its format: everything but where the trial's
    seam is and who is there to ask."""
    start = brief.index(FIRST_HEADING)
    return brief[start:brief.rindex(FENCE) + len(FENCE)]


class OneText(unittest.TestCase):
    def test_the_skill_holds_the_briefs_text_word_for_word(self):
        shared = shared_text(BRIEF.read_text(encoding="utf-8"))
        self.assertIn("## How to write it\n", shared)
        self.assertIn("## Format\n", shared)
        self.assertIn(shared, SKILL.read_text(encoding="utf-8"),
                      f"{SKILL.name} and {BRIEF.name} no longer say the same thing: change both together")


if __name__ == "__main__":
    unittest.main()
