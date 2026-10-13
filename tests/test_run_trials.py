"""Tests of the trial runner and the judge: what each condition puts before the agent.

    uv run --no-project python -m unittest discover -s tests

No session is launched: the tests stop at the trial's directory and at the command line.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TRIALS = Path(__file__).resolve().parents[1] / "trials"
RUN_TRIALS = TRIALS / "run_trials.py"
RUN_JUDGE = TRIALS / "judge" / "run_judge.py"
SEAM = TRIALS / "seams" / "triage_ticket"


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


class TrialDirectory(unittest.TestCase):
    """What the agent finds in its directory and in its system prompt, per condition."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.runner = load(RUN_TRIALS)
        self.runner.WORK_ROOT = Path(self._tmp.name)

    def prepare(self, condition: str) -> Path:
        return self.runner.prepare("sonnet", condition, "triage_ticket-04-1", SEAM)

    def files(self, work: Path) -> set[str]:
        return {p.relative_to(work).as_posix() for p in work.rglob("*") if p.is_file()}

    def test_without_has_only_the_seam(self):
        work = self.prepare("without")
        self.assertEqual(self.files(work), {"seam.py", "test.py", "README.md"})
        self.assertEqual(self.runner.system_prompt_args("without", work), [])

    def test_with_v2_has_the_charter_and_the_rule_setup_ships(self):
        work = self.prepare("with-v2")
        self.assertEqual(
            self.files(work),
            {"seam.py", "test.py", "README.md", "AGENTS.md", "evals/triage_ticket/charter.md"},
        )
        rule = (work / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("charter at `evals/<seam>/charter.md`", rule)
        shipped = self.runner.SETUP_SKILL.read_text(encoding="utf-8")
        for line in rule.removeprefix("# AGENTS\n\n").splitlines():
            self.assertIn(line, shipped)
        self.assertIn(rule, self.runner.system_prompt_args("with-v2", work)[1])

    def test_rule_only_has_the_rule_and_no_charter(self):
        work = self.prepare("rule-only")
        self.assertEqual(self.files(work), {"seam.py", "test.py", "README.md", "AGENTS.md"})

    def test_rule_only_gets_the_wording_fixed_in_its_protocol(self):
        work = self.prepare("rule-only")
        rule = (work / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(rule.startswith("# AGENTS\n\n## Stochastic seams\n"))
        self.assertIn(rule.removeprefix("# AGENTS\n\n").strip(),
                      (TRIALS / "protocol-rule-only.md").read_text(encoding="utf-8"))
        self.assertNotIn("charter", rule)
        self.assertNotIn("evals/", rule)
        self.assertIn(rule, self.runner.system_prompt_args("rule-only", work)[1])


class CommandLine(unittest.TestCase):
    """Both scripts take the condition; nothing matches the trial id, so nothing runs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.runs = Path(self._tmp.name)

    def test_the_runner_takes_every_condition(self):
        for condition in ("without", "with-v2", "rule-only"):
            done = command(RUN_TRIALS, condition, "--model", "sonnet", "--only", "none",
                           "--runs", str(self.runs))
            self.assertEqual((done.returncode, done.stdout.strip()), (0, "0 trials to run"), done.stderr)

    def test_the_judge_takes_every_condition(self):
        for condition in ("without", "with-v2", "rule-only"):
            (self.runs / "sonnet" / condition).mkdir(parents=True)
            done = command(RUN_JUDGE, condition, "--model", "sonnet", "--runs", str(self.runs))
            self.assertEqual((done.returncode, done.stdout.strip()), (0, "0 trials to judge"), done.stderr)


if __name__ == "__main__":
    unittest.main()
