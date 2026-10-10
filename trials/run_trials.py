"""Run the charter trials: each request given to a coding agent on a fresh copy of its seam.

    uv run --no-project python trials/run_trials.py without [--only triage_ticket-01-1] [--parallel 4]

Each trial runs in its own directory under WORK_ROOT (CHARTER_TRIAL_WORK, by default
charter-trial in the system temporary directory), outside the repo, holding only the
seam's files. Its diff, the agent's final answer and the session's numbers land in
trials/runs/<condition>/<seam>-<request>-<repeat>/. A trial whose folder already holds
session.json is skipped, so an interrupted run resumes.
"""

import argparse
import concurrent.futures
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

TRIALS = Path(__file__).resolve().parent
SEAMS = TRIALS / "seams"
CHARTERS = TRIALS / "charters"
SETUP_SKILL = TRIALS.parent / "a4a" / "skills" / "setup" / "SKILL.md"
RUNS = TRIALS / "runs"
WORK_ROOT = Path(os.environ.get("CHARTER_TRIAL_WORK") or Path(tempfile.gettempdir()) / "charter-trial")

MODEL = "claude-sonnet-5-5"
REPEATS = 3
SEAM_FILES = ("seam.py", "test.py", "README.md")
IGNORED_DIRS = {"__pycache__", ".pytest_cache"}
TIMEOUT_SECONDS = 30 * 60

# The same session limits in both conditions: no skills, plugins, hooks, CLAUDE.md or MCP
# (--safe-mode), file tools and Python only, nothing else approved.
CLAUDE_ARGS = [
    "-p",
    "--model", MODEL,
    "--safe-mode",
    "--output-format", "json",
    "--tools", "Read,Edit,Write,Glob,Grep,Bash",
    "--allowedTools", "Read Edit Write Glob Grep Bash(python *) Bash(python3 *) Bash(py *)",
    "--permission-mode", "acceptEdits",
    "--permission-prompts", "none",
]


def trials(condition):
    for seam_dir in sorted(p for p in SEAMS.iterdir() if p.is_dir()):
        for request in sorted((seam_dir / "requests").glob("*.md")):
            for repeat in range(1, REPEATS + 1):
                trial_id = f"{seam_dir.name}-{request.stem}-{repeat}"
                yield trial_id, seam_dir, request, RUNS / condition / trial_id


def prepare(condition, trial_id, seam_dir):
    work = WORK_ROOT / condition / trial_id
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for name in SEAM_FILES:
        shutil.copy2(seam_dir / name, work / name)
    if condition == "with":
        charter = work / "evals" / seam_dir.name / "charter.md"
        charter.parent.mkdir(parents=True)
        shutil.copy2(CHARTERS / f"{seam_dir.name}.md", charter)
        (work / "AGENTS.md").write_text(agents_rule(), encoding="utf-8")
    return work


def agents_rule():
    """The `## Stochastic seams` section, read from the setup skill that ships it."""
    skill = SETUP_SKILL.read_text(encoding="utf-8")
    block = re.search(r"```md\n(.*?)\n\s*```", skill, re.DOTALL).group(1)
    return "# AGENTS\n\n" + textwrap.dedent(block) + "\n"


def system_prompt_args(condition, work):
    """--safe-mode skips AGENTS.md, so the rule reaches the agent the way Claude Code
    would load it: in the system prompt, under the same heading."""
    if condition != "with":
        return []
    rule = (work / "AGENTS.md").read_text(encoding="utf-8")
    return [
        "--append-system-prompt",
        f"Contents of {work / 'AGENTS.md'} (project instructions, checked into the codebase):\n\n{rule}",
    ]


def snapshot(directory):
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file() and not IGNORED_DIRS.intersection(path.relative_to(directory).parts):
            files[path.relative_to(directory).as_posix()] = path.read_text(encoding="utf-8")
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
    return env


def run(condition, trial_id, seam_dir, request, out):
    work = prepare(condition, trial_id, seam_dir)
    before = snapshot(work)
    completed = subprocess.run(
        [shutil.which("claude"), *CLAUDE_ARGS, *system_prompt_args(condition, work)],
        input=request.read_text(encoding="utf-8"),
        cwd=work,
        env=session_env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=TIMEOUT_SECONDS,
    )
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
        "model": MODEL,
        "request": request.relative_to(TRIALS).as_posix(),
        "exit_code": completed.returncode,
        **{key: result.get(key) for key in (
            "is_error", "subtype", "num_turns", "duration_ms", "total_cost_usd", "session_id",
        )},
    }
    if result.get("is_error"):
        session["stderr"] = completed.stderr[-2000:]
    (out / "session.json").write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    return trial_id, session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("condition", choices=("without", "with"))
    parser.add_argument("--only", nargs="*", help="trial ids to run, e.g. triage_ticket-01-1")
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args()

    todo = [
        t for t in trials(args.condition)
        if (not args.only or t[0] in args.only) and not (t[3] / "session.json").exists()
    ]
    print(f"{len(todo)} trials to run", flush=True)
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        futures = [pool.submit(run, args.condition, *t) for t in todo]
        for future in concurrent.futures.as_completed(futures):
            trial_id, session = future.result()
            status = "ERROR" if session.get("is_error") else "ok"
            print(f"{trial_id}: {status}, {session.get('num_turns')} turns", flush=True)


if __name__ == "__main__":
    sys.exit(main())
