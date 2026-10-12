"""The triage_ticket adapter says why a call to `claude` failed, without making a call."""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
SEAM_DIR = Path(__file__).resolve().parent.parent / "trials" / "evals" / "triage_ticket"
sys.path.insert(0, str(SEAM_DIR))

import system  # noqa: E402

TICKET = {"subject": "Charged twice", "body": "Please refund one charge.", "tier": "pro"}


class TriageAdapterTest(unittest.TestCase):
    def test_missing_claude_is_named(self):
        with mock.patch.object(system.shutil, "which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "claude is not on PATH"):
                system.run(TICKET)

    def test_a_crash_of_claude_keeps_its_stderr(self):
        crashed = subprocess.CompletedProcess([], 1, stdout="", stderr="not logged in")
        with mock.patch.object(system.shutil, "which", return_value="claude"), \
                mock.patch.object(system.subprocess, "run", return_value=crashed):
            with self.assertRaisesRegex(RuntimeError, "exited 1.*not logged in"):
                system.run(TICKET)


if __name__ == "__main__":
    unittest.main()
