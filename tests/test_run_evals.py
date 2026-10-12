"""Tests of the edd runner, through its command line on a fake evals root.

    uv run --no-project python -m unittest discover -s tests
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "a4a" / "skills" / "edd" / "scripts" / "run_evals.py"

# The fake seam: each case says, run by run, whether its output passes, and what a call costs.
# Every call is appended to calls.txt, so a test sees which cases were paid for.
SYSTEM = '''
from pathlib import Path
MODEL = "fake-model"
PROVIDER = "fake"
CALLS = Path(__file__).with_name("calls.txt")

def run(case_input):
    seen = CALLS.read_text().split() if CALLS.exists() else []
    n = seen.count(case_input["id"])
    with CALLS.open("a") as f:
        f.write(case_input["id"] + "\\n")
    outcomes = case_input["outcomes"]
    return {"output": outcomes[n % len(outcomes)], "cost": case_input.get("cost", 0.0)}
'''

GRADER = '''
def grade(case, result):
    return bool(result["output"])
'''


def case(case_id: str, outcomes: list[bool], core: bool = False, cost: float = 0.0, split: str = "dev") -> dict:
    return {"id": case_id, "split": split, "core": core, "expected": True, "tags": [],
            "input": {"id": case_id, "outcomes": outcomes, "cost": cost}}


class FakeEvals:
    """An evals root with one seam, `fake`, and the runner run against it."""

    def __init__(self, cases: list[dict]):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.seam = self.root / "fake"
        self.seam.mkdir()
        (self.seam / "system.py").write_text(SYSTEM, encoding="utf-8")
        (self.seam / "grader.py").write_text(GRADER, encoding="utf-8")
        self.write_cases(cases)

    def write_cases(self, cases: list[dict], name: str = "cases.jsonl") -> None:
        (self.seam / name).write_text("".join(json.dumps(c) + "\n" for c in cases), encoding="utf-8")

    def run(self, *args: str, eval_set: str | None = "cases.jsonl") -> subprocess.CompletedProcess:
        env = {k: v for k, v in os.environ.items() if k != "EVAL_SET"}
        if eval_set is not None:
            env["EVAL_SET"] = eval_set
        return subprocess.run([sys.executable, str(RUNNER), *args, "--root", str(self.root)],
                              capture_output=True, text=True, env=env, cwd=self.root)

    def calls(self) -> list[str]:
        path = self.seam / "calls.txt"
        return path.read_text().split() if path.exists() else []

    def close(self) -> None:
        self._tmp.cleanup()


class EvalSetFixture(unittest.TestCase):
    def setUp(self):
        self.evals = FakeEvals([case("a", [True], core=True), case("b", [True])])
        self.addCleanup(self.evals.close)

    def test_a_run_without_the_fixture_refuses_to_start_and_names_the_variable(self):
        done = self.evals.run("fake", "--target", "0.5", eval_set=None)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("EVAL_SET", done.stderr)
        self.assertEqual(self.evals.calls(), [])

    def test_the_fixture_is_logged_on_the_run_row(self):
        self.evals.write_cases([case("a", [True], core=True)], name="set-2.jsonl")
        done = self.evals.run("fake", "--target", "0.5", "--k", "1", eval_set="set-2.jsonl")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("| set-2.jsonl |", (self.evals.root / "log.md").read_text(encoding="utf-8"))


class CoreThenExtended(unittest.TestCase):
    def test_a_failing_core_set_stops_the_run_before_the_extended_set(self):
        evals = FakeEvals([case("core-1", [False], core=True), case("core-2", [True], core=True),
                           case("ext-1", [True]), case("ext-2", [True])])
        self.addCleanup(evals.close)
        done = evals.run("fake", "--target", "0.8", "--k", "1")
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertEqual(sorted(evals.calls()), ["core-1", "core-2"])

    def test_a_passing_core_set_runs_the_rest_once_and_scores_the_whole_set(self):
        evals = FakeEvals([case("core-1", [True], core=True), case("ext-1", [False]),
                           case("ext-2", [True]), case("ext-3", [True])])
        self.addCleanup(evals.close)
        done = evals.run("fake", "--target", "0.5", "--k", "1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(sorted(evals.calls()), ["core-1", "ext-1", "ext-2", "ext-3"])
        self.assertIn("extended set: 0.75", done.stdout)

    def test_held_out_cases_stay_out_of_a_dev_run(self):
        evals = FakeEvals([case("core-1", [True], core=True), case("ho-1", [True], core=True, split="heldout")])
        self.addCleanup(evals.close)
        done = evals.run("fake", "--target", "0.5", "--k", "1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(evals.calls(), ["core-1"])


if __name__ == "__main__":
    unittest.main()
