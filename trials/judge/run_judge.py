"""Judge trials with the rubric, blind to the condition.

    uv run --no-project python trials/judge/run_judge.py without [--only triage_ticket-01-1] [--parallel 4]

For each trial folder under trials/runs/<condition>/, the judge gets the rubric's
instructions and the five inputs, and its answer lands in verdict.md beside the trial.
A trial that already holds verdict.md is skipped.
"""

import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

JUDGE = Path(__file__).resolve().parent
TRIALS = JUDGE.parent
RUBRIC = JUDGE / "rubric.md"

MODEL = "claude-opus-5-5"
SEAM_FILES = ("seam.py", "test.py", "README.md")
TIMEOUT_SECONDS = 15 * 60

# What would reveal the condition: the charter file and the AGENTS.md rule in the diff,
# and any sentence of the answer naming them.
REVEALING_PATHS = re.compile(r"^(evals/|AGENTS\.md$)")
REVEALING_WORDS = re.compile(r"charter|AGENTS\.md|evals/", re.IGNORECASE)
SENTENCE = re.compile(r"[^.!?\n]*(?:[.!?]+|\n|$)")


def instructions():
    text = RUBRIC.read_text(encoding="utf-8")
    return text[text.index("## Instructions for the judge"):]


def blind_diff(diff):
    kept = []
    for chunk in re.split(r"(?m)^(?=--- (?:a/|/dev/null))", diff):
        names = re.findall(r"(?m)^(?:---|\+\+\+) (?:[ab]/)?(\S+)", chunk)[:2]
        if not any(REVEALING_PATHS.match(name) for name in names):
            kept.append(chunk)
    return "".join(kept)


def blind_answer(answer):
    def redact(sentence):
        lead = sentence[:len(sentence) - len(sentence.lstrip())]
        tail = "\n" if sentence.endswith("\n") else ""
        return lead + "[removed]" + tail
    return "".join(
        redact(s) if REVEALING_WORDS.search(s) else s for s in SENTENCE.findall(answer)
    )


def prompt(trial_dir):
    session = json.loads((trial_dir / "session.json").read_text(encoding="utf-8"))
    request = TRIALS / session["request"]
    seam_dir = request.parent.parent
    seam = seam_dir.name
    parts = [instructions(), "# The inputs\n"]
    parts.append("## 1. The seam before the change\n")
    for name in SEAM_FILES:
        parts.append(f"### {name}\n\n````\n{(seam_dir / name).read_text(encoding='utf-8')}````\n")
    parts.append(f"## 2. The charter\n\n````\n{(TRIALS / 'charters' / f'{seam}.md').read_text(encoding='utf-8')}````\n")
    parts.append(f"## 3. The request\n\n````\n{request.read_text(encoding='utf-8')}````\n")
    diff = blind_diff((trial_dir / "diff.patch").read_text(encoding="utf-8"))
    parts.append(f"## 4. The diff\n\n````diff\n{diff or '(no change)'}\n````\n")
    answer = blind_answer((trial_dir / "answer.md").read_text(encoding="utf-8"))
    parts.append(f"## 5. The agent's final answer\n\n````\n{answer}\n````\n")
    return "\n".join(parts)


def judge(trial_dir):
    completed = subprocess.run(
        [shutil.which("claude"), "-p", "--model", MODEL, "--safe-mode", "--tools", ""],
        input=prompt(trial_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=TIMEOUT_SECONDS,
    )
    if completed.returncode != 0:
        return trial_dir.name, f"ERROR {completed.returncode}: {completed.stderr[-500:]}"
    (trial_dir / "verdict.md").write_text(completed.stdout, encoding="utf-8")
    return trial_dir.name, "ok"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("condition", choices=("without", "with", "with-v2"))
    parser.add_argument("--only", nargs="*", help="trial ids to judge")
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args()

    runs = TRIALS / "runs" / args.condition
    todo = [
        d for d in sorted(runs.iterdir())
        if (d / "session.json").exists() and not (d / "verdict.md").exists()
        and (not args.only or d.name in args.only)
    ]
    print(f"{len(todo)} trials to judge", flush=True)
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        for trial_id, status in pool.map(judge, todo):
            print(f"{trial_id}: {status}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
