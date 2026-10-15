"""Tests of the trial runner and the judge: what each condition puts before the agent.

    uv run --no-project python -m unittest discover -s tests

No session is launched: the tests stop at the trial's directory and at the command line.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TRIALS = Path(__file__).resolve().parents[1] / "trials"
RUN_TRIALS = TRIALS / "run_trials.py"
RUN_JUDGE = TRIALS / "judge" / "run_judge.py"
WRITE_CHARTERS = TRIALS / "write_charters.py"
SEAM = TRIALS / "seams" / "triage_ticket"


def load(path: Path):
    # A script finds its neighbours the way it does when run: from its own directory.
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
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

    def test_auto_charter_has_the_agents_charter_not_the_users(self):
        self.runner.CHARTERS_AUTO = Path(self._tmp.name) / "charters-auto"
        self.runner.CHARTERS_AUTO.mkdir()
        (self.runner.CHARTERS_AUTO / "triage_ticket.md").write_text("written by an agent", encoding="utf-8")
        work = self.prepare("auto-charter")
        self.assertEqual(
            self.files(work),
            {"seam.py", "test.py", "README.md", "AGENTS.md", "evals/triage_ticket/charter.md"},
        )
        charter = work / "evals" / "triage_ticket" / "charter.md"
        self.assertEqual(charter.read_text(encoding="utf-8"), "written by an agent")

    def test_auto_charter_gets_the_rule_fixed_in_its_protocol(self):
        rule = self.runner.agents_rule("auto-charter")
        self.assertIn(rule.removeprefix("# AGENTS\n\n").strip(),
                      (TRIALS / "protocol-auto-charter.md").read_text(encoding="utf-8"))
        self.assertIn("Read a seam's charter before changing the seam", rule)


    def test_practice_charter_has_its_own_charter_and_the_rule_of_its_protocol(self):
        self.runner.CHARTERS_PRACTICE = Path(self._tmp.name) / "charters-practice"
        self.runner.CHARTERS_PRACTICE.mkdir()
        (self.runner.CHARTERS_PRACTICE / "triage_ticket.md").write_text("by the practices", encoding="utf-8")
        work = self.prepare("practice-charter")
        charter = work / "evals" / "triage_ticket" / "charter.md"
        self.assertEqual(charter.read_text(encoding="utf-8"), "by the practices")
        self.assertEqual(self.runner.agents_rule("practice-charter"), self.runner.agents_rule("auto-charter"))

    def drafts(self, model: str) -> None:
        self.runner.CHARTERS_AUTO = Path(self._tmp.name) / "charters-auto"
        (self.runner.CHARTERS_AUTO / model).mkdir(parents=True)
        for n in (1, 2, 3):
            (self.runner.CHARTERS_AUTO / model / f"triage_ticket-{n}.md").write_text(
                f"{model} draft {n}", encoding="utf-8")

    def test_drafted_gives_each_repeat_its_own_draft_and_the_rule_setup_ships(self):
        self.drafts("sonnet")
        for repeat in (1, 2, 3):
            work = self.runner.prepare("sonnet", "drafted", f"triage_ticket-04-{repeat}", SEAM)
            self.assertEqual(
                self.files(work),
                {"seam.py", "test.py", "README.md", "AGENTS.md", "evals/triage_ticket/charter.md"},
            )
            charter = work / "evals" / "triage_ticket" / "charter.md"
            self.assertEqual(charter.read_text(encoding="utf-8"), f"sonnet draft {repeat}")
        self.assertEqual(self.runner.agents_rule("drafted"), self.runner.agents_rule("with-v2"))

    def test_drafted_gives_a_model_the_drafts_it_wrote(self):
        self.drafts("sonnet")
        self.drafts("haiku")
        work = self.runner.prepare("haiku", "drafted", "triage_ticket-06-2", SEAM)
        charter = work / "evals" / "triage_ticket" / "charter.md"
        self.assertEqual(charter.read_text(encoding="utf-8"), "haiku draft 2")


class CharterWriter(unittest.TestCase):
    """What the agent that writes a charter finds in its directory."""

    def test_it_sees_the_brief_and_the_seam_and_nothing_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = load(WRITE_CHARTERS)
            writer.WORK_ROOT = Path(tmp)
            work = writer.prepare(SEAM)
            self.assertEqual({p.relative_to(work).as_posix() for p in work.rglob("*")},
                             {"brief.md", "seam.py", "test.py", "README.md"})
            self.assertEqual((work / "brief.md").read_text(encoding="utf-8"),
                             (TRIALS / "brief-auto-charter.md").read_text(encoding="utf-8"))

    def test_the_practice_kind_gets_the_brief_with_the_practices(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = load(WRITE_CHARTERS)
            writer.WORK_ROOT = Path(tmp)
            work = writer.prepare(SEAM, "practice")
            self.assertEqual({p.relative_to(work).as_posix() for p in work.rglob("*")},
                             {"brief.md", "seam.py", "test.py", "README.md"})
            self.assertEqual((work / "brief.md").read_text(encoding="utf-8"),
                             (TRIALS / "brief-practice-charter.md").read_text(encoding="utf-8"))

    def test_each_draft_of_each_model_has_its_own_session_and_its_own_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = load(WRITE_CHARTERS)
            writer.WORK_ROOT = Path(tmp)
            works = {writer.prepare(SEAM, "auto", model, n) for model in ("sonnet", "haiku") for n in (1, 2, 3)}
            self.assertEqual(len(works), 6)
            for work in works:
                self.assertEqual({p.relative_to(work).as_posix() for p in work.rglob("*")},
                                 {"brief.md", "seam.py", "test.py", "README.md"})
            self.assertEqual(writer.destination("auto", "triage_ticket", "haiku", 2),
                             writer.CHARTERS_AUTO / "haiku" / "triage_ticket-2.md")

    def test_three_drafts_per_seam_are_to_write_and_one_already_there_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = load(WRITE_CHARTERS)
            writer.CHARTERS_AUTO = Path(tmp)
            (Path(tmp) / "haiku").mkdir()
            (Path(tmp) / "haiku" / "triage_ticket-2.md").write_text("written once", encoding="utf-8")
            todo = writer.to_write("auto", "haiku", ["triage_ticket"])
            self.assertEqual([(seam.name, n) for seam, n in todo], [("triage_ticket", 1), ("triage_ticket", 3)])
            self.assertEqual(len(writer.to_write("auto", "sonnet", None)), 12)

    def test_the_practice_kind_still_writes_one_charter_per_seam_where_it_did(self):
        writer = load(WRITE_CHARTERS)
        self.assertEqual(writer.destination("practice", "triage_ticket", "sonnet", None),
                         writer.CHARTERS_PRACTICE / "triage_ticket.md")


def trial_dir(root: Path, model: str) -> Path:
    """A trial as the runner leaves it, ready to be judged."""
    trial = root / "triage_ticket-04-1"
    trial.mkdir()
    (trial / "session.json").write_text(json.dumps(
        {"request": "seams/triage_ticket/requests/04.md", "model": model}), encoding="utf-8")
    (trial / "diff.patch").write_text("", encoding="utf-8")
    (trial / "answer.md").write_text("Done.", encoding="utf-8")
    return trial


class Judge(unittest.TestCase):
    """Who judges whom, what the judge may not learn, and what a verdict costs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.judge = load(RUN_JUDGE)

    def test_opus_judges_sonnet_and_sonnet_judges_haiku(self):
        root = Path(self._tmp.name)
        (root / "s").mkdir()
        (root / "h").mkdir()
        self.assertEqual(self.judge.judge_model(trial_dir(root / "s", "claude-sonnet-5-5")), "claude-opus-5-5")
        self.assertEqual(self.judge.judge_model(trial_dir(root / "h", "claude-haiku-5-5")), "claude-sonnet-5-5")

    def test_a_sentence_naming_haiku_is_removed_from_the_answer(self):
        blind = self.judge.blind_answer("I fixed the cap. As Haiku I cannot run the tests. Done.")
        self.assertNotIn("Haiku", blind)
        self.assertIn("I fixed the cap.", blind)

    def test_a_verdict_is_saved_with_what_it_cost(self):
        trial = trial_dir(Path(self._tmp.name), "claude-sonnet-5-5")
        answer = json.dumps({"result": "| F1 | held | not touched |\n", "total_cost_usd": 0.1234, "is_error": False})
        done = subprocess.CompletedProcess([], 0, stdout=answer, stderr="")
        with mock.patch.object(self.judge.subprocess, "run", return_value=done) as run:
            self.judge.judge(trial)
        self.assertIn("json", run.call_args.args[0])
        self.assertEqual((trial / "verdict.md").read_text(encoding="utf-8"), "| F1 | held | not touched |\n")
        record = json.loads((trial / "judge.json").read_text(encoding="utf-8"))
        self.assertEqual(record["model"], "claude-opus-5-5")
        self.assertEqual(record["cost_usd"], 0.1234)

    def test_a_judge_that_fails_leaves_no_verdict(self):
        trial = trial_dir(Path(self._tmp.name), "claude-sonnet-5-5")
        answer = json.dumps({"result": "Not logged in", "total_cost_usd": 0, "is_error": True})
        done = subprocess.CompletedProcess([], 1, stdout=answer, stderr="")
        with mock.patch.object(self.judge.subprocess, "run", return_value=done):
            _, status = self.judge.judge(trial)
        self.assertIn("ERROR", status)
        self.assertFalse((trial / "verdict.md").exists())


class CommandLine(unittest.TestCase):
    """Both scripts take the condition; nothing matches the trial id, so nothing runs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.runs = Path(self._tmp.name)

    def test_the_runner_takes_every_condition(self):
        for condition in ("without", "with-v2", "rule-only", "auto-charter", "practice-charter", "drafted"):
            done = command(RUN_TRIALS, condition, "--model", "sonnet", "--only", "none",
                           "--runs", str(self.runs))
            self.assertEqual((done.returncode, done.stdout.strip()), (0, "0 trials to run"), done.stderr)

    def test_haiku_is_an_agent_for_the_runner_the_judge_and_the_writer(self):
        (self.runs / "haiku" / "drafted").mkdir(parents=True)
        for script, args, nothing in (
            (RUN_TRIALS, ("drafted", "--only", "none", "--runs", str(self.runs)), "0 trials to run"),
            (RUN_JUDGE, ("drafted", "--runs", str(self.runs)), "0 trials to judge"),
            (WRITE_CHARTERS, ("auto", "--only", "none"), "0 charters to write"),
        ):
            done = command(script, *args, "--model", "haiku")
            self.assertEqual((done.returncode, done.stdout.strip()), (0, nothing), done.stderr)

    def test_the_judge_takes_every_condition(self):
        for condition in ("without", "with-v2", "rule-only", "auto-charter", "practice-charter", "drafted"):
            (self.runs / "sonnet" / condition).mkdir(parents=True)
            done = command(RUN_JUDGE, condition, "--model", "sonnet", "--runs", str(self.runs))
            self.assertEqual((done.returncode, done.stdout.strip()), (0, "0 trials to judge"), done.stderr)


HAS_REPS = (load(RUN_TRIALS).REPS / ".git").exists()


class RepsCases(unittest.TestCase):
    """The chosen REPS cases say where they start and which line and seams they are judged on."""

    def test_each_chosen_case_has_a_parent_a_request_one_line_and_its_seams(self):
        runner, judge = load(RUN_TRIALS), load(RUN_JUDGE)
        for name, parent in (("E1", "674648c"), ("E2", "a9b2c50"), ("E7", "521bce2"), ("E5", "f82c382"),
                             ("E6", "ed911df"), ("D3", "d9ee707"), ("D4", "c2e8e2a")):
            folder, found, seams = runner.reps_case(name)
            self.assertEqual(found, parent, name)
            self.assertTrue((folder / "request.md").read_text(encoding="utf-8").strip(), name)
            self.assertEqual(len(judge.charter_lines(folder.name)), 1, name)
            self.assertTrue(all(where.startswith("`src/") for where in seams.values()), name)
        self.assertEqual(list(runner.reps_case("E1")[2]), ["entrance", "planner"])

    def test_the_session_holds_no_provider_key(self):
        runner = load(RUN_TRIALS)
        with mock.patch.dict(runner.os.environ, {"GROQ_API_KEY": "x", "OPENROUTER_API_KEY": "y"}):
            env = runner.session_env()
        self.assertNotIn("GROQ_API_KEY", env)
        self.assertNotIn("OPENROUTER_API_KEY", env)

    def test_a_session_that_times_out_is_a_failed_trial_not_a_crash(self):
        runner = load(RUN_TRIALS)
        with tempfile.TemporaryDirectory() as tmp:
            runner.WORK_ROOT = Path(tmp) / "work"
            timeout = runner.subprocess.TimeoutExpired(["claude"], 1)
            with mock.patch.object(runner.subprocess, "run", side_effect=timeout):
                _, session = runner.run("sonnet", "without", "triage_ticket-04-1", SEAM,
                                        SEAM / "requests" / "04.md", Path(tmp) / "out")
        self.assertTrue(session["is_error"])


@unittest.skipUnless(HAS_REPS, "no REPS clone")
class RepsTrial(unittest.TestCase):
    """What a replay's agent finds in its directory and in its system prompt, per condition."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.runner = load(RUN_TRIALS)
        self.runner.WORK_ROOT = Path(self._tmp.name) / "work"
        self.runner.CHARTERS_AUTO = Path(self._tmp.name) / "drafts"

    def draft(self, case: str, seam: str, n: int) -> None:
        path = self.runner.CHARTERS_AUTO / "opus" / f"{case}-{seam}-{n}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {seam} charter, draft {n}\n", encoding="utf-8")

    def prepare(self, condition: str, trial_id: str) -> Path:
        folder = self.runner.reps_case(trial_id.rsplit("-", 1)[0])[0]
        return self.runner.prepare("opus", condition, trial_id, folder)

    def test_without_is_reps_at_the_parent_with_no_repository_and_its_own_instructions(self):
        work = self.prepare("without", "D4-1")
        self.assertTrue((work / "docs/work/15c-portfolio-ready/issues/01-a-plan-is-answered-in-words-too.md").exists())
        for absent in (".git", "evals", "AGENTS.md", ".env"):
            self.assertFalse((work / absent).exists(), absent)
        claude_md = (work / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertNotIn("## Stochastic seams", claude_md)
        self.assertIn(claude_md, self.runner.system_prompt_args("without", work)[1])

    def test_drafted_gives_each_repeat_its_own_draft_of_every_seam_and_the_rule_in_claude_md(self):
        for seam in ("entrance", "planner"):
            for n in (1, 2, 3):
                self.draft("D3", seam, n)
        work = self.prepare("drafted", "D3-2")
        for seam in ("entrance", "planner"):
            self.assertEqual((work / "evals" / seam / "charter.md").read_text(encoding="utf-8"),
                             f"# {seam} charter, draft 2\n")
        claude_md = (work / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertTrue(claude_md.startswith("# REPS"))
        rule = claude_md[claude_md.index("## Stochastic seams"):]
        shipped = self.runner.SETUP_SKILL.read_text(encoding="utf-8")
        for line in rule.splitlines():
            self.assertIn(line.strip(), shipped)
        self.assertFalse((work / "AGENTS.md").exists())
        self.assertIn(rule, self.runner.system_prompt_args("drafted", work)[1])

    def test_a_draft_missing_stops_the_trial_before_it_starts(self):
        with self.assertRaises(FileNotFoundError):
            self.prepare("drafted", "D4-3")

    def test_the_diff_leaves_out_the_install_and_any_file_that_is_not_text(self):
        work = self.prepare("without", "D4-1")
        self.assertTrue((work / ".venv").exists())
        before = self.runner.snapshot(work)
        (work / "README.md").write_text("changed\n", encoding="utf-8")
        (work / "docs" / "draft.md").write_text("a new draft\n", encoding="utf-8")
        (work / ".venv" / "x.py").write_text("ignored\n", encoding="utf-8")
        (work / "trainer.sqlite").write_bytes(b"SQLite format 3\x00\xff\xfe")
        diff = self.runner.unified_diff(before, self.runner.snapshot(work))
        self.assertIn("+++ b/README.md", diff)
        self.assertIn("+++ b/docs/draft.md", diff)
        self.assertNotIn("b/.venv", diff)
        self.assertNotIn("b/trainer.sqlite", diff)

    def test_a_replay_records_its_parent_and_lets_the_agent_run_uv(self):
        args = self.runner.claude_args(self.runner.reps_case("E1")[0])
        self.assertIn("Bash(uv *)", args[args.index("--allowedTools") + 1])
        self.assertNotIn("Bash(uv *)", " ".join(self.runner.claude_args(SEAM)))


@unittest.skipUnless(HAS_REPS, "no REPS clone")
class RepsCharterWriter(unittest.TestCase):
    """A REPS draft is written from the charter skill as the plugin ships it, in REPS at the parent."""

    def test_it_gets_the_skill_reps_at_the_parent_and_a_prompt_naming_the_seam(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = load(WRITE_CHARTERS)
            writer.WORK_ROOT = Path(tmp)
            work = writer.prepare_reps("E7", "planner", "opus", 1)
            self.assertEqual((work / "brief.md").read_text(encoding="utf-8"),
                             (TRIALS.parent / "a4a" / "skills" / "charter" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertFalse((work / "evals").exists())
            self.assertTrue((work / "src" / "trainer" / "coach" / "planner.py").exists())
            prompt = writer.reps_prompt("E7", "planner")
            self.assertIn("`planner`", prompt)
            self.assertIn("`evals/planner/charter.md`", prompt)

    def test_three_drafts_per_seam_of_a_case_and_one_already_there_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = load(WRITE_CHARTERS)
            writer.CHARTERS_AUTO = Path(tmp)
            (Path(tmp) / "opus").mkdir()
            (Path(tmp) / "opus" / "E1-planner-2.md").write_text("written once", encoding="utf-8")
            todo = writer.reps_to_write("opus", ["E1"])
            self.assertEqual(len(todo), 5)
            self.assertNotIn(("E1", "planner", 2), todo)


@unittest.skipUnless(HAS_REPS, "no REPS clone")
class RepsJudge(unittest.TestCase):
    """What the judge of a replay reads, and who it is."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.judge = load(RUN_JUDGE)

    def replay(self, case_dir: str, parent: str, diff: str = "", model: str = "claude-opus-5-5") -> Path:
        trial = Path(self._tmp.name) / f"{case_dir}-1"
        trial.mkdir()
        (trial / "session.json").write_text(json.dumps(
            {"request": f"reps/{case_dir}/request.md", "model": model, "parent": parent}), encoding="utf-8")
        (trial / "diff.patch").write_text(diff, encoding="utf-8")
        (trial / "answer.md").write_text("Done. As CLAUDE.md says, I stopped. Opus out.", encoding="utf-8")
        return trial

    def test_sonnet_judges_opus_5(self):
        trial = self.replay("E5-the-exclusion-vocabulary-as-an-enum", "f82c382", model="claude-opus-5")
        self.assertEqual(self.judge.judge_model(trial), "claude-sonnet-5-5")

    def test_it_reads_the_amendment_the_line_the_ticket_and_the_files_before_blind_to_the_charter(self):
        diff = ("--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n-x\n+y\n"
                "--- a/CLAUDE.md\n+++ b/CLAUDE.md\n@@ -1 +1 @@\n-x\n+y\n"
                "--- /dev/null\n+++ b/evals/planner/charter.md\n@@ -0,0 +1 @@\n+z\n")
        case = "E2-the-methodology-as-a-recipe"
        prompt = self.judge.prompt(self.replay(case, "a9b2c50", diff))
        self.assertIn("# A replay on a real project", prompt)
        self.assertIn((TRIALS / "reps" / case / "line.md").read_text(encoding="utf-8"), prompt)
        self.assertIn("# Nobody ever told the planner what a good workout is", prompt)
        self.assertIn("*Reasoning Engine for Personal Strength.*", prompt)
        inputs = prompt.split("# The inputs", 1)[1]
        self.assertNotIn("CLAUDE.md", inputs)
        self.assertNotIn("evals/planner", inputs)
        self.assertNotIn("Opus out", inputs)

    def test_a_ticket_missing_at_the_parent_is_said_so(self):
        trial = self.replay("E1-adaptation-bound-to-the-slot", "674648c")
        with mock.patch.object(self.judge, "at_parent", return_value=None):
            prompt = self.judge.prompt(trial)
        self.assertIn("(not in the project at that commit)", prompt)

    def test_a_replay_is_judged_once_its_verdict_has_the_lines_row(self):
        trial = self.replay("D4-a-plan-answered-in-words", "c2e8e2a")
        self.assertFalse(self.judge.judged(trial))
        (trial / "verdict.md").write_text("| C1 | held | not touched |\n", encoding="utf-8")
        self.assertTrue(self.judge.judged(trial))


class RepsCommandLine(unittest.TestCase):
    """The runner and the writer take REPS cases; nothing matches, so nothing runs."""

    def test_the_runner_and_the_writer_take_reps_cases(self):
        with tempfile.TemporaryDirectory() as runs:
            done = command(RUN_TRIALS, "without", "--model", "opus-5", "--reps", "E5", "--only", "none",
                           "--runs", runs)
            self.assertEqual((done.returncode, done.stdout.strip()), (0, "0 trials to run"), done.stderr)
        done = command(WRITE_CHARTERS, "reps", "--model", "opus", "--cases")
        self.assertEqual((done.returncode, done.stdout.strip()), (0, "0 charters to write"), done.stderr)


if __name__ == "__main__":
    unittest.main()
