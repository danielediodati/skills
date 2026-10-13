"""Have an agent write each seam's charter from its code alone, with nobody to ask.

    uv run --no-project python trials/write_charters.py [auto|practice] [--only triage_ticket] [--parallel 4]

Each seam gets one session, in its own directory under WORK_ROOT, holding the brief and the
seam's files. "auto" gives the brief that asks for the line as the code has it, "practice" the one
that says where a line belongs. The charter lands in trials/charters-<kind>/<seam>.md, with the
session's numbers in <seam>.session.json beside it. A seam that already has a charter there is
skipped: a charter is written once.
"""

import argparse
import concurrent.futures
import json
import shutil
import subprocess
import sys
from pathlib import Path

from run_trials import CHARTERS_AUTO, CHARTERS_PRACTICE, CLAUDE_ARGS, MODELS, SEAM_FILES, SEAMS
from run_trials import TIMEOUT_SECONDS, TRIALS, session_env
from run_trials import WORK_ROOT as TRIALS_WORK_ROOT

# Per kind of charter: the brief the writing agent gets, and where its charters land.
KINDS = {
    "auto": (TRIALS / "brief-auto-charter.md", CHARTERS_AUTO),
    "practice": (TRIALS / "brief-practice-charter.md", CHARTERS_PRACTICE),
}
WORK_ROOT = TRIALS_WORK_ROOT / "charter-writer"
MODEL = "sonnet"
PROMPT = "Read brief.md and do what it asks."


def prepare(seam_dir, kind="auto"):
    work = WORK_ROOT / kind / seam_dir.name
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copy2(KINDS[kind][0], work / "brief.md")
    for name in SEAM_FILES:
        shutil.copy2(seam_dir / name, work / name)
    return work


def write(seam_dir, kind="auto"):
    work = prepare(seam_dir, kind)
    charters = KINDS[kind][1]
    completed = subprocess.run(
        [shutil.which("claude"), *CLAUDE_ARGS, "--model", MODELS[MODEL]],
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
        "model": MODELS[MODEL],
        "exit_code": completed.returncode,
        "wrote_charter": charter.exists(),
        **{key: result.get(key) for key in (
            "is_error", "subtype", "num_turns", "duration_ms", "total_cost_usd", "session_id",
        )},
    }
    charters.mkdir(exist_ok=True)
    if charter.exists() and not result.get("is_error"):
        shutil.copy2(charter, charters / f"{seam_dir.name}.md")
        # The rules the agent gave itself, where its brief asks for them: kept to be read, not given to a trial.
        if (work / "principles.md").exists():
            shutil.copy2(work / "principles.md", charters / f"{seam_dir.name}.principles.md")
    (charters / f"{seam_dir.name}.session.json").write_text(
        json.dumps(session, indent=2) + "\n", encoding="utf-8")
    return seam_dir.name, session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", nargs="?", choices=KINDS, default="auto")
    parser.add_argument("--only", nargs="*", help="seams to write a charter for")
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args()

    todo = [
        d for d in sorted(p for p in SEAMS.iterdir() if p.is_dir())
        if (not args.only or d.name in args.only) and not (KINDS[args.kind][1] / f"{d.name}.md").exists()
    ]
    print(f"{len(todo)} charters to write", flush=True)
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        for seam, session in pool.map(lambda d: write(d, args.kind), todo):
            status = "ok" if session["wrote_charter"] and not session.get("is_error") else "ERROR"
            print(f"{seam}: {status}, {session.get('num_turns')} turns", flush=True)


if __name__ == "__main__":
    sys.exit(main())
