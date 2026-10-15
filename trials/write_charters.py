"""Have an agent write each seam's charter from its code alone, with nobody to ask.

    uv run --no-project python trials/write_charters.py [auto|practice] [--model sonnet]
        [--only triage_ticket] [--parallel 4]
    uv run --no-project python trials/write_charters.py reps --model opus --cases E1 D3

Each charter gets one session, in its own directory under WORK_ROOT, holding the brief and the
seam's files. "auto" gives the brief that asks for the line as the code has it, "practice" the one
that says where a line belongs.

"auto" writes three drafts per seam for the model, each from its own session, to
trials/charters-auto/<model>/<seam>-<n>.md. "practice" writes one per seam, to
trials/charters-practice/<seam>.md. The session's numbers land in a .session.json beside the
charter. A charter already there is skipped: a charter is written once and never edited.

"reps" writes three drafts for every seam a REPS case's line.md names, each from its own session in
REPS at the case's parent, to trials/charters-auto/<model>/<case>-<seam>-<n>.md. Its brief is the
`charter` skill as the plugin ships it, and the prompt names the seam, where it lives and where its
charter goes.
"""

import argparse
import concurrent.futures
import json
import shutil
import subprocess
import sys
from pathlib import Path

from run_trials import CHARTERS_AUTO, CHARTERS_PRACTICE, CLAUDE_ARGS, MODELS, SEAM_FILES, SEAMS
from run_trials import REPS_TIMEOUT_SECONDS, TIMEOUT_SECONDS, TRIALS, extract_reps, fresh, reps_case
from run_trials import session_env, system_prompt_args
from run_trials import WORK_ROOT as TRIALS_WORK_ROOT

# Per kind of charter: the brief the writing agent gets.
KINDS = {
    "auto": TRIALS / "brief-auto-charter.md",
    "practice": TRIALS / "brief-practice-charter.md",
    "reps": TRIALS.parent / "a4a" / "skills" / "charter" / "SKILL.md",
}
DRAFTS = 3  # per seam and model, for "auto": one for each repeat of a request
WORK_ROOT = TRIALS_WORK_ROOT / "charter-writer"
PROMPT = "Read brief.md and do what it asks."


def destination(kind, seam, model, n):
    """Where a charter lands: a numbered draft under its model for "auto", one per seam for "practice"."""
    if kind == "auto":
        return CHARTERS_AUTO / model / f"{seam}-{n}.md"
    return CHARTERS_PRACTICE / f"{seam}.md"


def to_write(kind, model, only):
    """Every (seam, draft number) that has no charter yet."""
    numbers = range(1, DRAFTS + 1) if kind == "auto" else (None,)
    return [
        (seam_dir, n)
        for seam_dir in sorted(p for p in SEAMS.iterdir() if p.is_dir())
        if not only or seam_dir.name in only
        for n in numbers
        if not destination(kind, seam_dir.name, model, n).exists()
    ]


def prepare(seam_dir, kind="auto", model="sonnet", n=1):
    work = WORK_ROOT / kind / model / (f"{seam_dir.name}-{n}" if kind == "auto" else seam_dir.name)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copy2(KINDS[kind], work / "brief.md")
    for name in SEAM_FILES:
        shutil.copy2(seam_dir / name, work / name)
    return work


def write(seam_dir, kind="auto", model="sonnet", n=1):
    work = prepare(seam_dir, kind, model, n)
    landed = destination(kind, seam_dir.name, model, n)
    completed = subprocess.run(
        [shutil.which("claude"), *CLAUDE_ARGS, "--model", MODELS[model]],
        input=PROMPT,
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
        result = {"is_error": True, "result": completed.stdout}
    charter = work / "charter.md"
    session = {
        "seam": seam_dir.name,
        "model": MODELS[model],
        "exit_code": completed.returncode,
        "wrote_charter": charter.exists(),
        **{key: result.get(key) for key in (
            "is_error", "subtype", "num_turns", "duration_ms", "total_cost_usd", "session_id",
        )},
    }
    landed.parent.mkdir(parents=True, exist_ok=True)
    if charter.exists() and not result.get("is_error"):
        shutil.copy2(charter, landed)
        # The rules the agent gave itself, where its brief asks for them: kept to be read, not given to a trial.
        if (work / "principles.md").exists():
            shutil.copy2(work / "principles.md", landed.with_suffix(".principles.md"))
    landed.with_suffix(".session.json").write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    return landed.stem, session


def reps_to_write(model, cases):
    """Every (case, seam, draft number) of the cases that has no draft yet."""
    return [
        (name, seam, n)
        for name in cases
        for seam in reps_case(name)[2]
        for n in range(1, DRAFTS + 1)
        if not (CHARTERS_AUTO / model / f"{name}-{seam}-{n}.md").exists()
    ]


def prepare_reps(name, seam, model, n):
    work = fresh(WORK_ROOT / "reps" / model / f"{name}-{seam}-{n}")
    extract_reps(reps_case(name)[1], work)
    shutil.copy2(KINDS["reps"], work / "brief.md")
    return work


def reps_prompt(name, seam):
    return (f"{PROMPT} The seam is `{seam}`, which lives in {reps_case(name)[2][seam]}. Write its charter "
            f"to `evals/{seam}/charter.md`. Nobody will answer questions: choose and carry on.")


def write_reps(name, seam, model, n):
    work = prepare_reps(name, seam, model, n)
    landed = CHARTERS_AUTO / model / f"{name}-{seam}-{n}.md"
    completed = subprocess.run(
        [shutil.which("claude"), *CLAUDE_ARGS, "--model", MODELS[model], *system_prompt_args("without", work)],
        input=reps_prompt(name, seam),
        cwd=work,
        env=session_env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=REPS_TIMEOUT_SECONDS,
    )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result = {"is_error": True, "result": completed.stdout}
    charter = work / "evals" / seam / "charter.md"
    session = {
        "case": name,
        "seam": seam,
        "model": MODELS[model],
        "exit_code": completed.returncode,
        "wrote_charter": charter.exists(),
        **{key: result.get(key) for key in (
            "is_error", "subtype", "num_turns", "duration_ms", "total_cost_usd", "session_id",
        )},
    }
    landed.parent.mkdir(parents=True, exist_ok=True)
    if charter.exists() and not result.get("is_error"):
        shutil.copy2(charter, landed)
    landed.with_suffix(".session.json").write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    return landed.stem, session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", nargs="?", choices=KINDS, default="auto")
    parser.add_argument("--cases", nargs="*", default=[], help="for reps: the cases whose seams get drafts")
    parser.add_argument("--model", choices=MODELS, default="sonnet", help="the model that writes")
    parser.add_argument("--only", nargs="*", help="seams to write a charter for")
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args()

    if args.kind == "reps":
        todo = reps_to_write(args.model, args.cases)
        write_one = lambda t: write_reps(*t[:2], args.model, t[2])  # noqa: E731
    else:
        todo = to_write(args.kind, args.model, args.only)
        write_one = lambda t: write(t[0], args.kind, args.model, t[1])  # noqa: E731
    print(f"{len(todo)} charters to write", flush=True)
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        for name, session in pool.map(write_one, todo):
            status = "ok" if session["wrote_charter"] and not session.get("is_error") else "ERROR"
            print(f"{name}: {status}, {session.get('num_turns')} turns, ${session.get('total_cost_usd')}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
