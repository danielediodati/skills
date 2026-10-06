#!/usr/bin/env python3
"""Eval runner for eval-driven development (the `edd` skill). Standard library only.

Copy into <project>/evals/ next to judge.py and calibrate.py. Layout, relative to evals/:

    <seam>/cases.jsonl   one case per line (FORMAT.md)
    <seam>/system.py     run(case_input) -> {"output": ..., "tokens"?: int, "seconds"?: float}
                         optional constants MODEL and PROVIDER
    <seam>/grader.py     grade(case, result) -> bool, or float in [0, 1] passing at >= 0.5
    <seam>/runs/         written here: one JSON per run, plus baseline-<split>.txt
    log.md               written here: one row per run

Examples:
    python evals/run_evals.py planner --speed smoke
    python evals/run_evals.py planner --k 3 --note "tool descriptions rewritten"
    python evals/run_evals.py planner --promote-last            # keep the change just measured
    python evals/run_evals.py planner --split heldout --k 3 --target 0.80
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ next to the seams: it would mark the tree dirty

SMOKE_FALLBACK = 8  # smoke subset size when no case is marked "smoke"
LOG_HEADER = (
    "| date | commit | seam | model | provider | split | speed | k | score | spread "
    "| gains/losses | cost/case | notes |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
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
    """Short content hash, used to detect a grader or case set changed since the baseline."""
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

def load_cases(seam_dir: Path, split: str, speed: str) -> list[dict]:
    """Read cases.jsonl, validate ids, and select the split and speed subset."""
    lines = (seam_dir / "cases.jsonl").read_text(encoding="utf-8").splitlines()
    cases = [json.loads(line) for line in lines if line.strip()]
    dupes = [i for i, n in Counter(c["id"] for c in cases).items() if n > 1]
    if dupes:
        sys.exit(f"duplicate case ids: {sorted(dupes)}")
    for c in cases:
        if c.get("expected") is None and not c.get("rubric"):
            print(f"warning: case {c['id']} has neither expected nor rubric", file=sys.stderr)
    cases = [c for c in cases if c.get("split", "dev") == split]
    if speed == "smoke":
        marked = [c for c in cases if c.get("smoke")]
        cases = marked or sorted(cases, key=lambda c: c["id"])[:SMOKE_FALLBACK]
    if not cases:
        sys.exit(f"no {split} cases for speed {speed} in {seam_dir}")
    return cases


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
    """Keep the change just measured: mark the latest full run of the split as its baseline."""
    runs_dir = root / seam / "runs"
    runs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(runs_dir.glob("*.json"))]
    runs = [r for r in runs if r["split"] == split and r["speed"] == "full"]
    if not runs:
        sys.exit(f"no full {split} run to promote in {runs_dir}")
    last = runs[-1]  # run ids start with a timestamp, so file order is time order
    (runs_dir / f"baseline-{split}.txt").write_text(last["run_id"], encoding="utf-8")
    append_log(root, [datetime.now().strftime("%Y-%m-%d"), last["commit"], seam, last["model"],
                      last["provider"], split, "promote", last["k"], f"{last['score']:.2f}", "-", "-", "-",
                      "; ".join(x for x in (f"promoted {last['run_id']}", note) if x)])
    print(f"promoted {last['run_id']} (score {last['score']:.2f}) to baseline for {split}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one seam's evals (edd skill).")
    parser.add_argument("seam", help="directory name under the evals root")
    parser.add_argument("--split", default="dev", choices=["dev", "heldout"])
    parser.add_argument("--speed", default="full", choices=["smoke", "full"])
    parser.add_argument("--k", type=int, default=None, help="runs per case (default: 1 smoke, 3 full)")
    parser.add_argument("--workers", type=int, default=1, help="cases run in parallel (1 for local CPU models)")
    parser.add_argument("--note", default="", help="the one change under test")
    parser.add_argument("--baseline", default=None, help="run id to compare against (default: promoted baseline)")
    parser.add_argument("--promote", action="store_true", help="make this run the baseline for its split")
    parser.add_argument("--promote-last", action="store_true",
                        help="run nothing: make the latest full run of this split the baseline")
    parser.add_argument("--target", type=float, default=None, help="exit 1 when the score is below this")
    parser.add_argument("--model", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent), help="evals root directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    seam_dir = root / args.seam
    runs_dir = seam_dir / "runs"
    k = args.k or (1 if args.speed == "smoke" else 3)
    if k % 2 == 0:
        sys.exit("use an odd k, so a case's majority is never a tie")
    if args.promote and args.speed == "smoke":
        sys.exit("smoke runs steer, they never decide: promote a full run")
    if args.promote_last:
        return promote_last(root, args.seam, args.split, args.note)

    sys.path[:0] = [str(seam_dir), str(root)]  # graders can import judge.py from the evals root
    system = load_module(seam_dir / "system.py", f"{args.seam}_system")
    grader = load_module(seam_dir / "grader.py", f"{args.seam}_grader")
    cases = load_cases(seam_dir, args.split, args.speed)
    model = args.model or getattr(system, "MODEL", "?")
    provider = args.provider or getattr(system, "PROVIDER", "?")
    commit = git_commit(root)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        results = list(pool.map(lambda c: run_case(c, system, grader, k), cases))

    # Score: mean over the k runs of the fraction of cases passed; spread: min to max of those.
    per_run = [sum(r["outcomes"][j] for r in results) / len(results) for j in range(k)]
    score = sum(per_run) / k
    spread = f"{min(per_run):.2f} to {max(per_run):.2f}"

    now = datetime.now()
    run_id = now.strftime("%Y%m%dT%H%M%S") + f"{now.microsecond // 1000:03d}-" + commit.replace("+", "-")
    run = {
        "run_id": run_id, "seam": args.seam, "split": args.split, "speed": args.speed, "k": k,
        "model": model, "provider": provider, "commit": commit, "note": args.note,
        "cases_hash": file_hash(seam_dir / "cases.jsonl"),
        "grader_hash": file_hash(seam_dir / "grader.py"),
        "per_run": per_run, "score": score, "results": results,
    }

    # Build the report first, persist the run, print last: a broken console never loses a run.
    report = [f"{args.seam} | {args.split} | {args.speed} | k={k} | {model} ({provider}) | {commit}",
              f"score {score:.2f} (spread {spread}) over {len(results)} cases"]
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
        if args.speed == "full":
            args.promote = True
            notes.append("first baseline")
        report.append("no baseline for this split yet" + ("; this run becomes it" if args.promote else ""))
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
        if baseline["grader_hash"] != run["grader_hash"]:
            report.append("WARNING grader.py changed since the baseline: run the unchanged system with the "
                          "new grader and promote that run before testing a system change (moving goalposts)")
        if baseline["cases_hash"] != run["cases_hash"]:
            report.append(f"note: cases.jsonl changed since the baseline; paired comparison uses the "
                          f"{len(common)} shared cases")
        if args.speed == "full":
            beyond = score > max(baseline["per_run"])
            report.append(f"beyond noise: {'yes' if beyond else 'no'} "
                          f"({score:.2f} vs baseline max {max(baseline['per_run']):.2f})")

    met = None if args.target is None else score >= args.target
    if met is not None:
        report.append(f"target {args.target:.2f}: {'met' if met else 'not met'}")

    # Persist the run, then the baseline marker and the log row.
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / f"{run_id}.json").write_text(json.dumps(run, indent=1), encoding="utf-8")
    if args.promote:
        (runs_dir / f"baseline-{args.split}.txt").write_text(run_id, encoding="utf-8")
        notes.append("promoted")
        report.append(f"promoted {run_id} to baseline for {args.split}")
    append_log(root, [datetime.now().strftime("%Y-%m-%d"), commit, args.seam, model, provider,
                      args.split, args.speed, k, f"{score:.2f}", spread, paired,
                      fmt_cost(results), "; ".join(notes) or "-"])
    report.append(f"run saved: {runs_dir / (run_id + '.json')}")
    try:
        print("\n".join(report))
    except (BrokenPipeError, UnicodeEncodeError):
        pass  # the run and the log row are already on disk
    return 1 if met is False else 0


if __name__ == "__main__":
    sys.exit(main())
