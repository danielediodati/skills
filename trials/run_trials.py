"""Run the charter trials: each request given to a coding agent on a fresh copy of its seam.

    uv run --no-project python trials/run_trials.py without --model sonnet [--requests 04 05]
        [--only triage_ticket-04-1] [--parallel 4] [--runs DIR]
    uv run --no-project python trials/run_trials.py without --model opus --reps E1 E2 [--only E1-2]

Each trial runs in its own directory under WORK_ROOT (CHARTER_TRIAL_WORK, by default
charter-trial in the system temporary directory), outside the repo, holding only the
seam's files. Its diff, the agent's final answer and the session's numbers land in
trials/runs/<model>/<condition>/<seam>-<request>-<repeat>/. A trial whose folder already holds a
session.json without an error is skipped, so an interrupted or failed run resumes.

With --reps, a trial replays a case from trials/reps/ instead: its directory is REPS at the case's
parent commit, from `git archive` (REPS is never touched, and no .env comes with it), installed with
`uv sync`. REPS's CLAUDE.md reaches the agent in both conditions, and in "drafted" the rule is
appended to it, where setup puts it in a project with no AGENTS.md.
"""

import argparse
import concurrent.futures
import difflib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import textwrap
from pathlib import Path

TRIALS = Path(__file__).resolve().parent
SEAMS = TRIALS / "seams"
CHARTERS = TRIALS / "charters"
SETUP_SKILL = TRIALS.parent / "a4a" / "skills" / "setup" / "SKILL.md"
# Written by an agent from the code, read by nobody. Session 3's four are at the top; the drafts of
# "drafted", three per seam and model, are in <model>/<seam>-<n>.md.
CHARTERS_AUTO = TRIALS / "charters-auto"
RULE_ONLY_PROTOCOL = TRIALS / "protocol-rule-only.md"
AUTO_CHARTER_PROTOCOL = TRIALS / "protocol-auto-charter.md"
# Written by an agent from the code and the practices that say where a line belongs.
CHARTERS_PRACTICE = TRIALS / "charters-practice"
PRACTICE_CHARTER_PROTOCOL = TRIALS / "protocol-practice-charter.md"
RUNS = TRIALS / "runs"
WORK_ROOT = Path(os.environ.get("CHARTER_TRIAL_WORK") or Path(tempfile.gettempdir()) / "charter-trial")

# The real project whose drift episodes trials/reps/ holds, one folder per case: a clone in REPS_DIR,
# by default next to this repo.
REPS = Path(os.environ.get("REPS_DIR") or TRIALS.parent.parent / "REPS")
REPS_CASES = TRIALS / "reps"

# "opus-5" replays the REPS cases Opus 5 made.
MODELS = {"sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5", "haiku": "claude-haiku-5-5",
          "opus-5": "claude-opus-5"}
REPEATS = 3
SEAM_FILES = ("seam.py", "test.py", "README.md")
# Left out of the diff, with any file that is not text: what installing and testing REPS write.
IGNORED_DIRS = {"__pycache__", ".pytest_cache", ".venv", ".mypy_cache", ".ruff_cache"}
TIMEOUT_SECONDS = 30 * 60
REPS_TIMEOUT_SECONDS = 90 * 60
# The providers REPS calls: a key left in the environment would let a replay spend on them.
PROVIDER_KEYS = re.compile(r"^(GROQ|OPENROUTER|OLLAMA|TELEGRAM|LANGSMITH|LANGCHAIN|ENTRANCE|LLM_BACKEND)")

# The same session limits in both conditions: no skills, plugins, hooks, CLAUDE.md or MCP
# (--safe-mode), file tools and Python only, nothing else approved.
CLAUDE_ARGS = [
    "-p",
    "--safe-mode",
    "--output-format", "json",
    "--tools", "Read,Edit,Write,Glob,Grep,Bash",
    "--allowedTools", "Read Edit Write Glob Grep Bash(python *) Bash(python3 *) Bash(py *)",
    "--permission-mode", "acceptEdits",
    "--permission-prompts", "none",
]
# A REPS replay also runs the project's tests, through uv.
REPS_ALLOWED = "Read Edit Write Glob Grep Bash(uv *) Bash(python *) Bash(python3 *) Bash(py *)"


def trials(runs, model, condition, requests=None):
    for seam_dir in sorted(p for p in SEAMS.iterdir() if p.is_dir()):
        for request in sorted((seam_dir / "requests").glob("*.md")):
            if requests and request.stem not in requests:
                continue
            for repeat in range(1, REPEATS + 1):
                trial_id = f"{seam_dir.name}-{request.stem}-{repeat}"
                yield trial_id, seam_dir, request, runs / model / condition / trial_id


def reps_case(name):
    """A REPS case: its folder, its parent commit from the README's row, and the seams its line.md names."""
    folder = next(REPS_CASES.glob(f"{name}-*"))
    row = next(r for r in (REPS_CASES / "README.md").read_text(encoding="utf-8").splitlines()
               if r.startswith(f"| [{name}]"))
    parent = row.split("|")[2].strip().strip("`")
    seams = re.search(r"(?m)^Seams: (.*)$", (folder / "line.md").read_text(encoding="utf-8")).group(1)
    return folder, parent, dict(re.fullmatch(r"(\w+) \((.*)\)", s).groups() for s in seams.split("; "))


def reps_trials(runs, model, condition, cases):
    for name in cases:
        folder = reps_case(name)[0]
        for repeat in range(1, REPEATS + 1):
            trial_id = f"{name}-{repeat}"
            yield trial_id, folder, folder / "request.md", runs / model / condition / trial_id


def fresh(work):
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    return work


def extract_reps(parent, work):
    """REPS's tracked files at the parent commit, with no repository, installed."""
    archive = subprocess.run(["git", "-C", str(REPS), "archive", "--format=tar", parent],
                             capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(work, filter="data")
    subprocess.run(["uv", "sync", "--frozen", "--quiet"], cwd=work, env=session_env(), check=True,
                   capture_output=True)


def prepare_reps(model, condition, trial_id, case_dir):
    name, repeat = trial_id.rsplit("-", 1)
    _, parent, seams = reps_case(name)
    work = fresh(WORK_ROOT / model / condition / trial_id)
    extract_reps(parent, work)
    if condition == "drafted":
        for seam in seams:
            charter = work / "evals" / seam / "charter.md"
            charter.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(CHARTERS_AUTO / model / f"{name}-{seam}-{repeat}.md", charter)
        claude_md = work / "CLAUDE.md"
        rule = agents_rule(condition).removeprefix("# AGENTS\n\n")
        claude_md.write_text(claude_md.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + rule, encoding="utf-8")
    return work


def prepare(model, condition, trial_id, seam_dir):
    if seam_dir.parent == REPS_CASES:
        return prepare_reps(model, condition, trial_id, seam_dir)
    work = fresh(WORK_ROOT / model / condition / trial_id)
    for name in SEAM_FILES:
        shutil.copy2(seam_dir / name, work / name)
    if condition not in ("without", "rule-only"):
        charter = work / "evals" / seam_dir.name / "charter.md"
        charter.parent.mkdir(parents=True)
        shutil.copy2(charter_source(model, condition, trial_id, seam_dir.name), charter)
    if condition != "without":
        (work / "AGENTS.md").write_text(agents_rule(condition), encoding="utf-8")
    return work


def charter_source(model, condition, trial_id, seam):
    """The charter a trial is given. "drafted": the draft the agent's own model wrote, a different
    one for each repeat of a request."""
    if condition == "drafted":
        repeat = trial_id.rsplit("-", 1)[1]
        return CHARTERS_AUTO / model / f"{seam}-{repeat}.md"
    charters = {"auto-charter": CHARTERS_AUTO, "practice-charter": CHARTERS_PRACTICE}.get(condition, CHARTERS)
    return charters / f"{seam}.md"


def agents_rule(condition):
    """The `## Stochastic seams` section, read from the setup skill that ships it; for
    "rule-only", "auto-charter" and "practice-charter", the wording their protocols fix."""
    source = {
        "rule-only": RULE_ONLY_PROTOCOL,
        "auto-charter": AUTO_CHARTER_PROTOCOL,
        "practice-charter": PRACTICE_CHARTER_PROTOCOL,
    }.get(condition, SETUP_SKILL)
    skill = source.read_text(encoding="utf-8")
    block = re.search(r"```md\n(.*?)\n\s*```", skill, re.DOTALL).group(1)
    return "# AGENTS\n\n" + textwrap.dedent(block) + "\n"


def system_prompt_args(condition, work):
    """--safe-mode skips AGENTS.md and CLAUDE.md, so they reach the agent the way Claude Code
    would load them: in the system prompt, under the same heading. A project's own CLAUDE.md
    reaches it in every condition."""
    instructions = work / "CLAUDE.md"
    if not instructions.exists():
        if condition == "without":
            return []
        instructions = work / "AGENTS.md"
    text = instructions.read_text(encoding="utf-8")
    return [
        "--append-system-prompt",
        f"Contents of {instructions} (project instructions, checked into the codebase):\n\n{text}",
    ]


def snapshot(directory):
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file() and not IGNORED_DIRS.intersection(path.relative_to(directory).parts):
            try:
                files[path.relative_to(directory).as_posix()] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
    return files


def unified_diff(before, after):
    chunks = []
    for name in sorted(set(before) | set(after)):
        old, new = before.get(name, ""), after.get(name, "")
        if old != new:
            chunks.extend(difflib.unified_diff(
                old.splitlines(keepends=True),
                new.splitlines(keepends=True),
                fromfile=f"a/{name}" if name in before else "/dev/null",
                tofile=f"b/{name}" if name in after else "/dev/null",
            ))
    return "".join(line if line.endswith("\n") else line + "\n" for line in chunks)


def session_env():
    """This interpreter first on PATH, so `python -m unittest` works in the trial."""
    env = dict(os.environ)
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), env.get("PATH", "")))
    return {key: value for key, value in env.items() if not PROVIDER_KEYS.match(key)}


def claude_args(seam_dir):
    if seam_dir.parent != REPS_CASES:
        return CLAUDE_ARGS
    allowed = CLAUDE_ARGS.index("--allowedTools") + 1
    return [*CLAUDE_ARGS[:allowed], REPS_ALLOWED, *CLAUDE_ARGS[allowed + 1:]]


def run(model, condition, trial_id, seam_dir, request, out):
    work = prepare(model, condition, trial_id, seam_dir)
    before = snapshot(work)
    try:
        completed = subprocess.run(
            [shutil.which("claude"), *claude_args(seam_dir), "--model", MODELS[model],
             *system_prompt_args(condition, work)],
            input=request.read_text(encoding="utf-8"),
            cwd=work,
            env=session_env(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=REPS_TIMEOUT_SECONDS if seam_dir.parent == REPS_CASES else TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        # A failed trial, run again on the next pass; the others go on.
        completed = subprocess.CompletedProcess([], None, stdout="", stderr="timeout")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result = {"is_error": True, "result": completed.stdout, "stderr": completed.stderr}

    out.mkdir(parents=True, exist_ok=True)
    (out / "diff.patch").write_text(unified_diff(before, snapshot(work)), encoding="utf-8")
    (out / "answer.md").write_text(result.get("result") or "", encoding="utf-8")
    session = {
        "trial": trial_id,
        "condition": condition,
        "model": MODELS[model],
        "request": request.relative_to(TRIALS).as_posix(),
        **({"parent": reps_case(trial_id.rsplit("-", 1)[0])[1]} if seam_dir.parent == REPS_CASES else {}),
        "exit_code": completed.returncode,
        **{key: result.get(key) for key in (
            "is_error", "subtype", "num_turns", "duration_ms", "total_cost_usd", "session_id",
        )},
    }
    if result.get("is_error"):
        session["stderr"] = completed.stderr[-2000:]
    (out / "session.json").write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    return trial_id, session


def done(out):
    """A trial is done once it has a session that did not fail; a failed one runs again."""
    session = out / "session.json"
    return session.exists() and not json.loads(session.read_text(encoding="utf-8")).get("is_error")


def main():
    parser = argparse.ArgumentParser()
    # "with-v2" and later: the charter and the rule as setup/SKILL.md ships it now.
    # "rule-only": no charter, and the rule as trials/protocol-rule-only.md words it.
    # "auto-charter": a charter from trials/charters-auto/, and the rule as its protocol words it.
    # "practice-charter": a charter from trials/charters-practice/, and the rule as its protocol words it.
    # "drafted": a draft the agent's own model wrote, one per repeat, and the rule as setup/SKILL.md ships it.
    parser.add_argument("condition", choices=(
        "without", "with", "with-v2", "rule-only", "auto-charter", "practice-charter", "drafted"))
    parser.add_argument("--model", choices=MODELS, required=True, help="the coding agent")
    parser.add_argument("--requests", nargs="*", help="request names to run, e.g. 04 05")
    parser.add_argument("--reps", nargs="*", help="REPS cases to replay instead of the seams, e.g. E1 D3")
    parser.add_argument("--only", nargs="*", help="trial ids to run, e.g. triage_ticket-01-1")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--runs", type=Path, default=RUNS, help="where runs land; a dry check goes elsewhere")
    args = parser.parse_args()

    source = (reps_trials(args.runs.resolve(), args.model, args.condition, args.reps) if args.reps is not None
              else trials(args.runs.resolve(), args.model, args.condition, args.requests))
    todo = [t for t in source if (not args.only or t[0] in args.only) and not done(t[3])]
    print(f"{len(todo)} trials to run", flush=True)
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        futures = [pool.submit(run, args.model, args.condition, *t) for t in todo]
        for future in concurrent.futures.as_completed(futures):
            trial_id, session = future.result()
            status = "ERROR" if session.get("is_error") else "ok"
            print(f"{trial_id}: {status}, {session.get('num_turns')} turns", flush=True)


if __name__ == "__main__":
    sys.exit(main())
