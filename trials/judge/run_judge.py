"""Judge trials with the rubric, blind to the condition and to the agent's model.

    uv run --no-project python trials/judge/run_judge.py without --model sonnet
        [--only triage_ticket-04-1] [--parallel 4] [--redo] [--runs DIR]

For each trial folder under trials/runs/<model>/<condition>/, the judge gets the rubric's
instructions and the five inputs, and its answer lands in verdict.md beside the trial.
The judge is the model that did not run the trial, read from its session.json, and is
recorded in judge.json. A trial whose verdict has a row for every charter line is skipped;
a verdict missing a line is judged again.
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

# Each model's trials are judged by the other one.
JUDGES = {"claude-sonnet-5-5": "claude-opus-5-5", "claude-opus-5-5": "claude-sonnet-5-5"}
AGENTS = ("sonnet", "opus")  # the folders under trials/runs/
SEAM_FILES = ("seam.py", "test.py", "README.md")
TIMEOUT_SECONDS = 15 * 60

# What would reveal the condition: the charter file and the AGENTS.md rule in the diff,
# and any sentence of the answer naming them. A sentence naming a model would reveal the agent.
REVEALING_PATHS = re.compile(r"^(evals/|AGENTS\.md$)")
REVEALING_WORDS = re.compile(r"charter|AGENTS\.md|evals/|\bsonnet\b|\bopus\b", re.IGNORECASE)
# A dot inside a word ("AGENTS.md", "seam.py") does not end the sentence.
SENTENCE = re.compile(r"(?:[^.!?\n]|[.!?]+(?=[^\s.!?]))*(?:[.!?]+|\n|$)")


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


def charter_lines(seam):
    """The ids the rubric gives the charter's bullets: F1... free, C1... constrained, B1... budget."""
    ids, prefix, count = [], None, 0
    for line in (TRIALS / "charters" / f"{seam}.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            prefix = {"## Free": "F", "## Constrained": "C", "## Target and budget": "B"}.get(line.strip())
            count = 0
        elif prefix and line.startswith("- "):
            count += 1
            ids.append(f"{prefix}{count}")
    return ids


def missing_lines(verdict, seam):
    """Charter lines the verdict has no row for: the judge must answer every one."""
    rows = set(re.findall(r"(?m)^\|\s*([FCB]\d+)\s*\|", verdict))
    return [line for line in charter_lines(seam) if line not in rows]


def seam_of(trial_dir):
    session = json.loads((trial_dir / "session.json").read_text(encoding="utf-8"))
    return session["request"].split("/")[1]


def judged(trial_dir):
    """A trial is judged once its verdict has a row for every line; an incomplete one is judged again."""
    verdict = trial_dir / "verdict.md"
    return verdict.exists() and not missing_lines(verdict.read_text(encoding="utf-8"), seam_of(trial_dir))


def judge_model(trial_dir):
    session = json.loads((trial_dir / "session.json").read_text(encoding="utf-8"))
    return JUDGES[session["model"]]


def judge(trial_dir):
    model = judge_model(trial_dir)
    completed = subprocess.run(
        [shutil.which("claude"), "-p", "--model", model, "--safe-mode", "--tools", ""],
        input=prompt(trial_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=TIMEOUT_SECONDS,
    )
    if completed.returncode != 0:
        return trial_dir.name, f"ERROR {completed.returncode}: {completed.stderr[-500:]}"
    (trial_dir / "verdict.md").write_text(completed.stdout, encoding="utf-8")
    missing = missing_lines(completed.stdout, seam_of(trial_dir))
    record = {"model": model, "missing_lines": missing}
    (trial_dir / "judge.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    if missing:
        return trial_dir.name, f"INCOMPLETE, judged by {model}: no row for {', '.join(missing)}"
    return trial_dir.name, f"ok, judged by {model}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("condition", choices=("without", "with", "with-v2", "rule-only", "auto-charter"))
    parser.add_argument("--model", choices=AGENTS, required=True, help="the coding agent whose trials are judged")
    parser.add_argument("--only", nargs="*", help="trial ids to judge")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--redo", action="store_true", help="judge again trials that have a verdict")
    parser.add_argument("--runs", type=Path, default=TRIALS / "runs", help="where the runs are")
    args = parser.parse_args()

    runs = args.runs.resolve() / args.model / args.condition
    todo = [
        d for d in sorted(runs.iterdir())
        if (d / "session.json").exists() and (args.redo or not judged(d))
        and (not args.only or d.name in args.only)
    ]
    print(f"{len(todo)} trials to judge", flush=True)
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        for trial_id, status in pool.map(judge, todo):
            print(f"{trial_id}: {status}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
