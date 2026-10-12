#!/usr/bin/env python3
"""Eval runner for eval-driven development (the `edd` skill). Standard library only.

Copy into <project>/evals/ next to judge.py and calibrate.py. Layout, relative to evals/:

    <seam>/<eval set>    one case per line (FORMAT.md), named by the EVAL_SET environment variable
    <seam>/system.py     run(case_input) -> {"output": ..., "tokens"?: int, "seconds"?: float}
                         optional constants MODEL and PROVIDER
    <seam>/grader.py     grade(case, result) -> bool, or float in [0, 1] passing at >= 0.5
    <seam>/runs/         written here: one JSON per run, plus baseline-<split>.txt
    log.md               written here: one row per run

A run goes in the order of decision 11: the core set first, then the extended set (every case of
the split) only if the core set reaches the target. A change that fails the core set is rejected
without a call spent on the rest.

Examples:
    EVAL_SET=cases.jsonl python evals/run_evals.py planner --target 0.80 --note "tool descriptions rewritten"
    EVAL_SET=cases.jsonl python evals/run_evals.py planner --promote-last   # keep the change just measured
    EVAL_SET=cases.jsonl python evals/run_evals.py planner --split heldout --target 0.80
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ next to the seams: it would mark the tree dirty

EVAL_SET_VAR = "EVAL_SET"  # names the eval set, a file in the seam's directory, never a path in the code
LOG_HEADER = (
    "| date | commit | seam | eval set | model | provider | split | set | k | score | spread "
    "| gains/losses | cost/case | notes |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
)


# ---------- helpers shared with calibrate.py ----------

def load_module(path: Path, name: str):
    """Import a seam's system.py or grader.py from its path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        sys.exit(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_hash(path: Path) -> str:
    """Short content hash, used to detect a grader or eval set changed since the baseline."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.exists() else "-"


def git_commit(root: Path) -> str:
    """Short commit id, marked +dirty when the tree has changes other than eval outputs."""
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root,
                             capture_output=True, text=True, check=True).stdout.strip()
        top = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root,
                                  capture_output=True, text=True, check=True).stdout.strip())
        status = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                                capture_output=True, text=True, check=True).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        return "nogit"
    try:
        evals_rel = root.resolve().relative_to(top.resolve()).as_posix()
    except ValueError:  # evals root outside the repository: every change counts
        evals_rel = None

    def is_eval_output(line: str) -> bool:
        # Files this runner writes do not count as a change to the system under test.
        path = line[3:].strip().strip('"')
        if "__pycache__" in path:
            return True
        if evals_rel is None:
            return False
        prefix = "" if evals_rel == "." else f"{evals_rel}/"
        return path == f"{prefix}log.md" or (path.startswith(prefix) and "/runs/" in f"/{path}")

    dirty = any(not is_eval_output(line) for line in status if line.strip())
    return sha + ("+dirty" if dirty else "")


def append_log(root: Path, cells: list) -> None:
    """Append one row to log.md, creating the table header on first use."""
    log = root / "log.md"
    if not log.exists():
        log.write_text("# Eval log\n\n" + LOG_HEADER, encoding="utf-8")
    row = "| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |\n"
    with log.open("a", encoding="utf-8") as f:
        f.write(row)


# ---------- running a seam ----------

def eval_set_path(seam_dir: Path) -> Path:
    """The eval set named in the environment. A run without it refuses to start."""
    name = os.environ.get(EVAL_SET_VAR)
    if not name:
        sys.exit(f"{EVAL_SET_VAR} is not set: name the eval set in the environment, "
                 f"e.g. {EVAL_SET_VAR}=cases.jsonl for {seam_dir / 'cases.jsonl'}")
    path = seam_dir / name
    if not path.is_file():
        sys.exit(f"{EVAL_SET_VAR}={name}: no such eval set in {seam_dir}")
    return path


def load_cases(path: Path, split: str) -> tuple[list[dict], list[dict]]:
    """Read the eval set, validate it, and return the split's core cases and the rest."""
    lines = path.read_text(encoding="utf-8").splitlines()
    cases = [json.loads(line) for line in lines if line.strip()]
    dupes = [i for i, n in Counter(c["id"] for c in cases).items() if n > 1]
    if dupes:
        sys.exit(f"duplicate case ids: {sorted(dupes)}")
    for c in cases:
        if c.get("expected") is None and not c.get("rubric"):
            print(f"warning: case {c['id']} has neither expected nor rubric", file=sys.stderr)
    cases = [c for c in cases if c.get("split", "dev") == split]
    core = [c for c in cases if c.get("core")]
    if not core:
        sys.exit(f"no core {split} cases in {path}: mark the core set with \"core\": true (FORMAT.md)")
    return core, [c for c in cases if not c.get("core")]


def run_case(case: dict, system, grader, k: int) -> dict:
    """Run one case k times. A run passes when the grader says so; the case when most runs pass."""
    outcomes, tokens, seconds, errors = [], [], [], []
    for _ in range(k):
        start = time.perf_counter()
        try:
            result = system.run(case["input"])
        except Exception as exc:  # a crash of the system is a failed run
            outcomes.append(False)
            errors.append(f"system: {type(exc).__name__}: {exc}")
            continue
        seconds.append(result.get("seconds", time.perf_counter() - start))
        if result.get("tokens") is not None:
            tokens.append(result["tokens"])
        try:
            score = grader.grade(case, result)
        except Exception as exc:  # a crash of the grader is a grader bug: recorded apart
            outcomes.append(False)
            errors.append(f"grader: {type(exc).__name__}: {exc}")
            continue
        outcomes.append(score >= 0.5 if isinstance(score, float) else bool(score))
    return {
        "id": case["id"],
        "tags": case.get("tags", []),
        "outcomes": outcomes,
        "passed": sum(outcomes) > k / 2,
        "tokens": sum(tokens) / len(tokens) if tokens else None,
        "seconds": sum(seconds) / len(seconds) if seconds else None,
        "errors": errors,
    }


def run_cases(cases: list[dict], system, grader, k: int, workers: int) -> list[dict]:
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        return list(pool.map(lambda c: run_case(c, system, grader, k), cases))


def scores(results: list[dict], k: int) -> tuple[float, list[float]]:
    """Score: mean over the k runs of the fraction of cases passed; per_run: those k fractions."""
    per_run = [sum(r["outcomes"][j] for r in results) / len(results) for j in range(k)]
    return sum(per_run) / k, per_run


def sign_test(gains: int, losses: int) -> float:
    """One-sided sign test: probability of at least `gains` heads in gains + losses fair flips."""
    n = gains + losses
    if n == 0:
        return 1.0
    return sum(math.comb(n, i) for i in range(gains, n + 1)) / 2 ** n


def read_baseline(runs_dir: Path, split: str, wanted: str | None) -> dict | None:
    """The run named by --baseline, else the promoted baseline for this split, else None."""
    run_id = wanted
    marker = runs_dir / f"baseline-{split}.txt"
    if run_id is None and marker.exists():
        run_id = marker.read_text(encoding="utf-8").strip()
    if run_id is None:
        return None
    path = runs_dir / f"{run_id}.json"
    if not path.exists():
        sys.exit(f"baseline run {run_id} not found in {runs_dir}")
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_cost(results: list[dict]) -> str:
    """Mean tokens and seconds per case run, for the log's cost column."""
    toks = [r["tokens"] for r in results if r["tokens"] is not None]
    secs = [r["seconds"] for r in results if r["seconds"] is not None]
    parts = []
    if toks:
        parts.append(f"{sum(toks) / len(toks) / 1000:.1f}k tok")
    if secs:
        parts.append(f"{sum(secs) / len(secs):.1f} s")
    return ", ".join(parts) or "-"


def promote_last(root: Path, seam: str, split: str, note: str) -> int:
    """Keep the change just measured: mark the latest extended run of the split as its baseline."""
    runs_dir = root / seam / "runs"
    runs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(runs_dir.glob("*.json"))]
    runs = [r for r in runs if r["split"] == split and r["set"] == "extended"]
    if not runs:
        sys.exit(f"no extended {split} run to promote in {runs_dir}")
    last = runs[-1]  # run ids start with a timestamp, so file order is time order
    (runs_dir / f"baseline-{split}.txt").write_text(last["run_id"], encoding="utf-8")
    append_log(root, [datetime.now().strftime("%Y-%m-%d"), last["commit"], seam, last["eval_set"],
                      last["model"], last["provider"], split, "promote", last["k"], f"{last['score']:.2f}",
                      "-", "-", "-", "; ".join(x for x in (f"promoted {last['run_id']}", note) if x)])
    print(f"promoted {last['run_id']} (score {last['score']:.2f}) to baseline for {split}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one seam's evals (edd skill).")
    parser.add_argument("seam", help="directory name under the evals root")
    parser.add_argument("--target", type=float, default=None,
                        help="the charter's target: the core set must reach it before the extended set runs")
    parser.add_argument("--split", default="dev", choices=["dev", "heldout"])
    parser.add_argument("--k", type=int, default=3, help="runs per case, odd")
    parser.add_argument("--workers", type=int, default=1, help="cases run in parallel (1 for local CPU models)")
    parser.add_argument("--note", default="", help="the one change under test")
    parser.add_argument("--baseline", default=None, help="run id to compare against (default: promoted baseline)")
    parser.add_argument("--promote", action="store_true", help="make this run the baseline for its split")
    parser.add_argument("--promote-last", action="store_true",
                        help="run nothing: make the latest extended run of this split the baseline")
    parser.add_argument("--model", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent), help="evals root directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    seam_dir = root / args.seam
    runs_dir = seam_dir / "runs"
    if args.k % 2 == 0:
        sys.exit("use an odd k, so a case's majority is never a tie")
    if args.promote_last:
        return promote_last(root, args.seam, args.split, args.note)
    eval_set = eval_set_path(seam_dir)
    if args.target is None:
        sys.exit("--target is required: the charter's target decides whether the extended set runs")

    sys.path[:0] = [str(seam_dir), str(root)]  # graders can import judge.py from the evals root
    system = load_module(seam_dir / "system.py", f"{args.seam}_system")
    grader = load_module(seam_dir / "grader.py", f"{args.seam}_grader")
    core, rest = load_cases(eval_set, args.split)
    model = args.model or getattr(system, "MODEL", "?")
    provider = args.provider or getattr(system, "PROVIDER", "?")
    commit = git_commit(root)
    k = args.k
    settings = {"seam": args.seam, "eval_set": eval_set.name, "split": args.split, "k": k,
                "model": model, "provider": provider, "commit": commit,
                "cases_hash": file_hash(eval_set), "grader_hash": file_hash(seam_dir / "grader.py")}

    # The core set first: a change that fails it is rejected without a call spent on the rest.
    core_results = run_cases(core, system, grader, k, args.workers)
    core_score, core_per_run = scores(core_results, k)
    core_run = save_run(root, runs_dir, settings, "core", core_results, core_score, core_per_run, args.note)
    report = [f"{args.seam} | {eval_set.name} | {args.split} | k={k} | {model} ({provider}) | {commit}",
              f"core set: {core_score:.2f} (spread {spread(core_per_run)}) over {len(core_results)} cases"]
    if core_score < args.target:
        report.append(f"target {args.target:.2f}: not met on the core set; the extended set "
                      f"({len(rest)} more cases) does not run")
        report.append(f"run saved: {runs_dir / (core_run + '.json')}")
        emit(report)
        return 1

    # The extended set: the whole split, reusing the core results already paid for.
    results = core_results + run_cases(rest, system, grader, k, args.workers)
    score, per_run = scores(results, k)
    report.append(f"extended set: {score:.2f} (spread {spread(per_run)}) over {len(results)} cases")
    tags = sorted({t for r in results for t in r["tags"]})
    if tags:
        by_tag = []
        for t in tags:
            tagged = [r for r in results if t in r["tags"]]
            by_tag.append(f"{t} {sum(r['passed'] for r in tagged) / len(tagged):.2f} ({len(tagged)})")
        report.append("by tag (cases passing by majority): " + ", ".join(by_tag))
    report.append(f"cost per case run: {fmt_cost(results)}")
    crashed = [r["id"] for r in results if r["errors"]]
    if crashed:
        report.append(f"errors in: {', '.join(crashed)} (details in the run file)")

    # Paired comparison against the baseline, over the cases both runs share.
    notes = [args.note] if args.note else []
    paired = "-"
    baseline = read_baseline(runs_dir, args.split, args.baseline)
    if baseline is None:
        args.promote = True
        notes.append("first baseline")
        report.append("no baseline for this split yet; this run becomes it")
    else:
        before = {r["id"]: r["passed"] for r in baseline["results"]}
        common = [r for r in results if r["id"] in before]
        gains = [r["id"] for r in common if r["passed"] and not before[r["id"]]]
        losses = [r["id"] for r in common if not r["passed"] and before[r["id"]]]
        p = sign_test(len(gains), len(losses))
        paired = f"+{len(gains)}/-{len(losses)} (p={p:.2f})"
        report.append(f"vs baseline {baseline['run_id']}: {paired} over {len(common)} shared cases")
        if gains:
            report.append(f"  gains: {', '.join(gains)}")
        if losses:
            report.append(f"  losses: {', '.join(losses)} (keeping this change accepts them)")
            notes.append(f"losses: {', '.join(losses)}")
        if baseline["grader_hash"] != settings["grader_hash"]:
            report.append("WARNING grader.py changed since the baseline: run the unchanged system with the "
                          "new grader and promote that run before testing a system change (moving goalposts)")
        if baseline["cases_hash"] != settings["cases_hash"]:
            report.append(f"note: the eval set changed since the baseline; paired comparison uses the "
                          f"{len(common)} shared cases")
        beyond = score > max(baseline["per_run"])
        report.append(f"beyond noise: {'yes' if beyond else 'no'} "
                      f"({score:.2f} vs baseline max {max(baseline['per_run']):.2f})")

    met = score >= args.target
    report.append(f"target {args.target:.2f}: {'met' if met else 'not met'}")
    if args.promote:
        notes.append("promoted")
    run_id = save_run(root, runs_dir, settings, "extended", results, score, per_run, "; ".join(notes),
                      paired=paired)
    if args.promote:
        (runs_dir / f"baseline-{args.split}.txt").write_text(run_id, encoding="utf-8")
        report.append(f"promoted {run_id} to baseline for {args.split}")
    report.append(f"run saved: {runs_dir / (run_id + '.json')}")
    emit(report)
    return 0 if met else 1


def spread(per_run: list[float]) -> str:
    return f"{min(per_run):.2f} to {max(per_run):.2f}"


def save_run(root: Path, runs_dir: Path, settings: dict, which: str, results: list[dict],
             score: float, per_run: list[float], notes: str, paired: str = "-") -> str:
    """Persist one run and its log row before anything is printed: a broken console never loses a run."""
    now = datetime.now()
    run_id = (now.strftime("%Y%m%dT%H%M%S") + f"{now.microsecond // 1000:03d}-{which}-"
              + settings["commit"].replace("+", "-"))
    run = {"run_id": run_id, **settings, "set": which, "note": notes,
           "per_run": per_run, "score": score, "results": results}
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / f"{run_id}.json").write_text(json.dumps(run, indent=1), encoding="utf-8")
    append_log(root, [now.strftime("%Y-%m-%d"), settings["commit"], settings["seam"], settings["eval_set"],
                      settings["model"], settings["provider"], settings["split"], which, settings["k"],
                      f"{score:.2f}", spread(per_run), paired, fmt_cost(results), notes or "-"])
    return run_id


def emit(report: list[str]) -> None:
    try:
        print("\n".join(report))
    except (BrokenPipeError, UnicodeEncodeError):
        pass  # the run and the log row are already on disk


if __name__ == "__main__":
    sys.exit(main())
