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

# The fake seam: each case says, run by run, whether its output passes. FAKE_COST in the
# environment is what one call costs, in dollars.
# FAKE_OUTCOMES in the environment overrides a case's outcomes, so the seam can get worse while the
# eval set stays the same.
# Every call is appended to calls.txt, so a test sees which cases were paid for.
SYSTEM = '''
import json, os
from pathlib import Path
MODEL = "fake-model"
PROVIDER = "fake"
COST_PER_CASE = float(os.environ.get("FAKE_COST", "0"))
CALLS = Path(__file__).with_name("calls.txt")

def run(case_input):
    seen = CALLS.read_text().split() if CALLS.exists() else []
    n = seen.count(case_input["id"])
    with CALLS.open("a") as f:
        f.write(case_input["id"] + "\\n")
    outcomes = json.loads(os.environ.get("FAKE_OUTCOMES", "{}")).get(case_input["id"], case_input["outcomes"])
    return {"output": outcomes[n % len(outcomes)], "cost": COST_PER_CASE}
'''

GRADER = '''
def grade(case, result):
    return bool(result["output"])
'''


def case(case_id: str, outcomes: list[bool], core: bool = False, split: str = "dev") -> dict:
    return {"id": case_id, "split": split, "core": core, "expected": True, "tags": [],
            "input": {"id": case_id, "outcomes": outcomes}}


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

    def run(self, *args: str, eval_set: str | None = "cases.jsonl",
            outcomes: dict | None = None, cost: float = 0.0) -> subprocess.CompletedProcess:
        env = {k: v for k, v in os.environ.items() if k not in ("EVAL_SET", "FAKE_OUTCOMES", "FAKE_COST")}
        env["FAKE_COST"] = str(cost)
        if eval_set is not None:
            env["EVAL_SET"] = eval_set
        if outcomes:
            env["FAKE_OUTCOMES"] = json.dumps(outcomes)
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


class TargetBesideTheEvalSet(unittest.TestCase):
    def setUp(self):
        self.evals = FakeEvals([case("core-1", [True], core=True), case("core-2", [False], core=True),
                                case("ext-1", [True])])
        self.addCleanup(self.evals.close)

    def write_target(self, target: str) -> None:
        (self.evals.seam / "eval.md").write_text(
            f"# fake eval\n\n- Target: {target}\n- Good: the output is true.\n", encoding="utf-8")

    def test_the_target_is_read_from_the_file_beside_the_eval_set(self):
        self.write_target("0.80 on the dev split")
        done = self.evals.run("fake", "--k", "1")
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertIn("target 0.80: not met on the core set", done.stdout)
        self.assertEqual(sorted(self.evals.calls()), ["core-1", "core-2"])

    def test_a_run_with_no_target_anywhere_refuses_to_start_and_names_the_file(self):
        done = self.evals.run("fake", "--k", "1")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("eval.md", done.stderr)
        self.assertEqual(self.evals.calls(), [])

    def test_a_file_with_no_target_line_refuses_to_start(self):
        (self.evals.seam / "eval.md").write_text("# fake eval\n\n- Good: the output is true.\n", encoding="utf-8")
        done = self.evals.run("fake", "--k", "1")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("eval.md", done.stderr)
        self.assertEqual(self.evals.calls(), [])

    def test_a_target_on_the_command_line_wins_and_the_report_says_so(self):
        self.write_target("0.80")
        done = self.evals.run("fake", "--target", "0.5", "--k", "1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("target 0.50", done.stdout)
        self.assertIn("eval.md says 0.80", done.stdout)


def ten_cases() -> list[dict]:
    """Ten core cases. c0 fails its second run, so the first run of the seam scores 0.97 with spread 0.10."""
    return [case("c0", [True, False, True], core=True)] + [case(f"c{i}", [True], core=True) for i in range(1, 10)]


class TargetAndBestResult(unittest.TestCase):
    def setUp(self):
        self.evals = FakeEvals(ten_cases())
        self.addCleanup(self.evals.close)
        first = self.evals.run("fake", "--target", "0.5")
        self.assertEqual(first.returncode, 0, first.stderr)

    def test_below_the_target_fails(self):
        done = self.evals.run("fake", "--target", "0.95", outcomes={"c1": [False]})
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("not met", done.stdout)

    def test_below_the_best_result_within_the_spread_passes_with_no_warning(self):
        done = self.evals.run("fake", "--target", "0.5", outcomes={"c1": [True, True, False]})
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertNotIn("WARNING", done.stdout)

    def test_below_the_best_result_beyond_the_spread_passes_with_a_warning(self):
        done = self.evals.run("fake", "--target", "0.5", outcomes={"c1": [False], "c2": [False], "c3": [False]})
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("WARNING below the best result", done.stdout)

    def test_a_grader_change_empties_the_best_results(self):
        with (self.evals.seam / "grader.py").open("a", encoding="utf-8") as f:
            f.write("# stricter, one day\n")
        done = self.evals.run("fake", "--target", "0.5", outcomes={"c1": [False], "c2": [False], "c3": [False]})
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("best results discarded", done.stdout)
        self.assertNotIn("WARNING", done.stdout)

    def test_an_eval_set_change_empties_the_best_results(self):
        self.evals.write_cases(ten_cases() + [case("c10", [True])])
        done = self.evals.run("fake", "--target", "0.5", outcomes={"c1": [False], "c2": [False], "c3": [False]})
        self.assertIn("best results discarded", done.stdout)
        self.assertNotIn("WARNING", done.stdout)


class CodeVersion(unittest.TestCase):
    def test_a_code_change_keeps_the_best_result_marked_as_measured_on_an_earlier_version(self):
        evals = FakeEvals(ten_cases())
        self.addCleanup(evals.close)
        self.assertEqual(evals.run("fake", "--target", "0.5").returncode, 0)
        first = evals.run("fake", "--target", "0.5")
        self.assertNotIn("earlier version", first.stdout)
        # The best result as if measured on a commit before this one.
        best_path = evals.seam / "best.json"
        best = json.loads(best_path.read_text(encoding="utf-8"))
        best["splits"]["dev"]["fake-model"]["code"] = "0a1b2c3"
        best_path.write_text(json.dumps(best), encoding="utf-8")
        done = evals.run("fake", "--target", "0.5", outcomes={"c1": [False], "c2": [False], "c3": [False]})
        self.assertIn("earlier version", done.stdout)
        self.assertIn("WARNING below the best result", done.stdout)


class Spending(unittest.TestCase):
    def setUp(self):
        self.evals = FakeEvals([case("core-1", [True], core=True), case("core-2", [True], core=True)]
                               + [case(f"ext-{i}", [True]) for i in range(10)])
        self.addCleanup(self.evals.close)

    def agree(self, budget: str) -> None:
        done = self.evals.run("--agree-budget", budget, "--note", "ticket 06", eval_set=None)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_a_paid_run_with_no_agreed_budget_refuses_to_start(self):
        done = self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.01)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("--agree-budget", done.stderr)
        self.assertEqual(self.evals.calls(), [])

    def test_a_free_run_needs_no_budget(self):
        done = self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.0)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_a_run_that_would_pass_the_budget_refuses_to_start_and_prints_the_total_and_the_budget(self):
        self.agree("0.01")
        done = self.evals.run("fake", "--target", "0.5", "--k", "3", cost=0.01)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("spent $0.00 of $0.01", done.stderr)
        self.assertEqual(self.evals.calls(), [])

    def test_the_running_total_is_reported_and_logged_after_every_run(self):
        self.agree("1.00")
        first = self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.01)
        self.assertIn("spent $0.12 of $1.00", first.stdout)
        second = self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.01)
        self.assertIn("spent $0.24 of $1.00", second.stdout)
        self.assertIn("| $0.24 |", (self.evals.root / "log.md").read_text(encoding="utf-8"))

    def test_a_run_whose_core_fits_but_whose_extended_set_would_pass_the_budget_does_not_start(self):
        self.agree("0.05")
        done = self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.01)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("spent $0.00 of $0.05", done.stderr)
        self.assertEqual(self.evals.calls(), [])

    def test_a_budget_raised_for_the_same_ticket_keeps_the_running_total(self):
        self.agree("1.00")
        self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.01)
        self.agree("2.00")
        done = self.evals.run("fake", "--check", "--k", "1", cost=0.01)
        self.assertIn("spent $0.12 of $2.00", done.stdout)

    def test_a_budget_for_another_ticket_starts_the_total_at_zero(self):
        self.agree("1.00")
        self.evals.run("fake", "--target", "0.5", "--k", "1", cost=0.01)
        done = self.evals.run("--agree-budget", "1.00", "--note", "ticket 07", eval_set=None)
        self.assertIn("spent $0.00 of $1.00", done.stdout)

    def test_the_check_spends_nothing_and_shows_the_estimate_against_the_budget(self):
        self.agree("1.00")
        done = self.evals.run("fake", "--check", "--k", "1", cost=0.01)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.evals.calls(), [])
        self.assertIn("$0.12", done.stdout)
        self.assertIn("spent $0.00 of $1.00", done.stdout)


if __name__ == "__main__":
    unittest.main()
