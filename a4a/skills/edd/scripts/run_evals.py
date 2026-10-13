#!/usr/bin/env python3
"""Eval runner for eval-driven development (the `edd` skill). Standard library only.

Copy into <project>/evals/ next to judge.py and calibrate.py. Layout, relative to evals/:

    <seam>/<eval set>    one case per line (FORMAT.md), named by the EVAL_SET environment variable
    <seam>/system.py     run(case_input) -> {"output": ..., "tokens"?: int, "seconds"?: float, "cost"?: float}
                         constants MODEL, PROVIDER and COST_PER_CASE (dollars per call, 0 when free);
                         --model sets MODEL before the first call, so run() reads it when it calls
    <seam>/grader.py     grade(case, result) -> bool, or float in [0, 1] passing at >= 0.5
    <seam>/eval.md       the seam's target, on a line "- Target: 0.80" (FORMAT.md)
    <seam>/runs/         written here: one JSON per run, with what the seam answered
    <seam>/best.json     written here: the best result of each model on each split
    log.md               written here: one row per run
    spending.json        written here: the spending budget agreed with the user, and what is spent

A run goes in the order of decision 11: the core set first, then the extended set (every case of
the split) only if the core set reaches the target. A change that fails the core set is rejected
without a call spent on the rest.

The extended run is judged as decisions 12 and 13 say. Below the target: failure, the only one.
Below this model's best result by more than the run-to-run spread: a warning. Best results are
kept per model with the code version they were measured on; a change to the grader or the eval
set discards them, a change to the code keeps them, marked as measured on an earlier version.
A case's tags are not part of the eval set for this: editing them discards nothing. A run below
the target is recorded and never kept as a best result.

Nothing paid runs without approval (decision 14). The user agrees a spending budget for the
ticket first (--agree-budget). A run whose estimated cost, core and extended sets together, would
take the total past the budget refuses to start and prints both; the check runs again before the
extended set, on what the core set really cost. Every run
reports and logs its cost and the running total. --check runs the free checks and shows the
estimate, without a call.

Examples:
    python evals/run_evals.py --agree-budget 2.00 --note "ticket 12"   # only once the user agreed it
    EVAL_SET=cases.jsonl python evals/run_evals.py planner --check
    EVAL_SET=cases.jsonl python evals/run_evals.py planner --note "tool descriptions rewritten"
    EVAL_SET=cases.jsonl python evals/run_evals.py planner --split heldout
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ next to the seams: it would mark the tree dirty

EVAL_SET_VAR = "EVAL_SET"  # names the eval set, a file in the seam's directory, never a path in the code
TARGET_FILE = "eval.md"  # beside the eval set: the seam's target and the direction of its eval set
SPENDING = "spending.json"
LOG_HEADER = (
    "| date | commit | seam | eval set | model | provider | split | set | k | score | spread "
    "| gains/losses | cost/case | cost | spent | notes |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
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
    """Short content hash, used to detect a grader changed since the best results."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.exists() else "-"


def eval_set_hash(path: Path) -> str:
    """Short hash of what the eval set measures: every case, without its tags. Tags describe a case
    (a failure category, a slice) and do not change it, so editing them discards no best result."""
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for c in cases:
        c.pop("tags", None)
    return hashlib.sha256(json.dumps(cases, sort_keys=True).encode("utf-8")).hexdigest()[:12]


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
        return path in (f"{prefix}log.md", f"{prefix}{SPENDING}") or (path.startswith(prefix) and (
            "/runs/" in f"/{path}" or path.endswith("/best.json")))

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
        if "input" not in c:
            sys.exit(f"case {c['id']} has no input")
        if c.get("split", "dev") not in ("dev", "heldout"):
            sys.exit(f"case {c['id']}: split must be dev or heldout, not {c['split']!r}")
        if not isinstance(c.get("core", False), bool):
            sys.exit(f"case {c['id']}: core must be true or false")
        if c.get("expected") is None and not c.get("rubric"):
            print(f"warning: case {c['id']} has neither expected nor rubric", file=sys.stderr)
    cases = [c for c in cases if c.get("split", "dev") == split]
    core = [c for c in cases if c.get("core")]
    if not core:
        sys.exit(f"no core {split} cases in {path}: mark the core set with \"core\": true (FORMAT.md)")
    return core, [c for c in cases if not c.get("core")]


def read_target(seam_dir: Path) -> float | None:
    """The target the seam declares beside its eval set, or None when it declares none."""
    path = seam_dir / TARGET_FILE
    if not path.is_file():
        return None
    found = re.search(r"(?m)^- Target:\s*([01](?:\.\d+)?)", path.read_text(encoding="utf-8"))
    return float(found.group(1)) if found else None


def run_case(case: dict, system, grader, k: int, per_call: float) -> dict:
    """Run one case k times. A run passes when the grader says so; the case when most runs pass.
    A call costs what the adapter reports, else the estimate per call."""
    outcomes, outputs, tokens, seconds, errors, cost = [], [], [], [], [], 0.0
    for _ in range(k):
        start = time.perf_counter()
        try:
            result = system.run(case["input"])
        except Exception as exc:  # a crash of the system is a failed run, and may still be paid
            outcomes.append(False)
            outputs.append(None)
            errors.append(f"system: {type(exc).__name__}: {exc}")
            cost += per_call
            continue
        cost += result["cost"] if result.get("cost") is not None else per_call
        outputs.append(result.get("output"))
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
        "outputs": outputs,  # what the seam answered, run by run: failures are read without paying again
        "passed": sum(outcomes) > k / 2,
        "tokens": sum(tokens) / len(tokens) if tokens else None,
        "seconds": sum(seconds) / len(seconds) if seconds else None,
        "errors": errors,
        "cost": cost,
    }


def run_cases(cases: list[dict], system, grader, k: int, workers: int, per_call: float) -> list[dict]:
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        return list(pool.map(lambda c: run_case(c, system, grader, k, per_call), cases))


# ---------- spending (decision 14) ----------

def cost_per_call(system, runs_dir: Path, model: str) -> float | None:
    """What one call costs: measured on this model's latest run, else the adapter's COST_PER_CASE."""
    for path in sorted(runs_dir.glob("*.json"), reverse=True):  # run ids start with a timestamp
        run = json.loads(path.read_text(encoding="utf-8"))
        if run.get("model") == model and run.get("results"):
            return sum(r["cost"] for r in run["results"]) / (run["k"] * len(run["results"]))
    return getattr(system, "COST_PER_CASE", None)


def read_spending(root: Path) -> dict | None:
    path = root / SPENDING
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def agree_budget(root: Path, budget: float, note: str) -> int:
    """Record the spending budget the user agreed for a ticket. A new budget for the same ticket keeps
    what is already spent against it; a budget for another ticket starts the total at zero."""
    spending = read_spending(root)
    if spending is None or spending.get("note") != note:
        spending = {"note": note, "spent": 0.0, "runs": []}
    spending.update(budget=budget, agreed=datetime.now().isoformat(timespec="seconds"))
    (root / SPENDING).write_text(json.dumps(spending, indent=1), encoding="utf-8")
    print(f"spending budget {money(budget)} agreed; {fmt_total(spending)}")
    return 0


def money(dollars: float) -> str:
    """Dollars to the cent, and a small amount to its two leading digits: half a cent reads $0.005,
    never $0.00."""
    if dollars <= 0 or dollars >= 0.1:
        return f"${dollars:.2f}"
    text = f"{dollars:.{1 - math.floor(math.log10(dollars))}f}"
    while text.endswith("0") and len(text.partition(".")[2]) > 2:
        text = text[:-1]
    return f"${text}"


def fmt_total(spending: dict | None) -> str:
    """The running total against the budget, as every report and every request for approval shows it."""
    if spending is None:
        return "no spending budget agreed"
    agreed_for = f" agreed for {spending['note']}" if spending.get("note") else ""
    return f"spent {money(spending['spent'])} of {money(spending['budget'])}{agreed_for}"


def refusal(spending: dict | None, estimate: float, what: str) -> str | None:
    """Why a run of this estimated cost may not start, or None when it may."""
    if estimate <= 0:
        return None
    if spending is None:
        return (f"{what} would cost about {money(estimate)} and no spending budget is agreed: agree one "
                f"with the user, then run --agree-budget <dollars>")
    if spending["spent"] + estimate > spending["budget"] + 1e-9:
        return (f"{what} would cost about {money(estimate)}; {fmt_total(spending)}: it would pass the "
                f"budget. Ask the user before anything else is paid")
    return None


def record_spending(root: Path, spending: dict | None, run_id: str, cost: float) -> None:
    if spending is None:
        return
    spending["spent"] += cost
    spending["runs"].append({"run_id": run_id, "cost": cost})
    (root / SPENDING).write_text(json.dumps(spending, indent=1), encoding="utf-8")


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


def load_best(seam_dir: Path, settings: dict) -> tuple[dict, str | None]:
    """The seam's best results, emptied when the grader or the eval set changed (decision 13)."""
    path = seam_dir / "best.json"
    fresh = {"eval_set": settings["eval_set"], "cases_hash": settings["cases_hash"],
             "grader_hash": settings["grader_hash"], "splits": {}}
    if not path.exists():
        return fresh, None
    best = json.loads(path.read_text(encoding="utf-8"))
    changed = [what for what, key in (("the grader", "grader_hash"), ("the eval set", "cases_hash"))
               if best.get(key) != settings[key]]
    if changed:
        return fresh, (f"{' and '.join(changed)} changed: best results discarded, "
                       f"the measure changed so earlier scores do not compare")
    return best, None


def verdict(score: float, per_run: list[float], target: float, best: dict | None) -> list[str]:
    """Decision 12: the target decides, the best result informs."""
    lines = [f"target {target:.2f}: {'met' if score >= target else 'not met: failure'}"]
    if best is None:
        return lines
    gap = best["score"] - score
    noise = max(max(per_run) - min(per_run), max(best["per_run"]) - min(best["per_run"]))
    if score >= target and gap > noise + 1e-9:
        lines.append(f"WARNING below the best result by {gap:.2f}, more than the run-to-run spread "
                     f"({noise:.2f}); not a failure, the target decides")
    return lines


def fmt_best(model: str, entry: dict, commit: str) -> str:
    """One best result, marked when it was measured on another version of the code."""
    aged = "" if entry["code"] == commit else f", an earlier version: {commit} now"
    return f"{model} {entry['score']:.2f} (spread {spread(entry['per_run'])}; {entry['run_id']}, code {entry['code']}{aged})"


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


def spread(per_run: list[float]) -> str:
    return f"{min(per_run):.2f} to {max(per_run):.2f}"


def save_run(root: Path, runs_dir: Path, settings: dict, which: str, results: list[dict],
             score: float, per_run: list[float], notes: str, paired: str = "-",
             cost: float | None = None, spent: float | None = None) -> str:
    """Persist one run and its log row before anything is printed: a broken console never loses a run.
    The cost is what this run paid for: the extended run reuses the core results, so it pays only
    for the rest of the set."""
    now = datetime.now()
    run_id = (now.strftime("%Y%m%dT%H%M%S") + f"{now.microsecond // 1000:03d}-{which}-"
              + settings["commit"].replace("+", "-"))
    cost = sum(r["cost"] for r in results) if cost is None else cost
    run = {"run_id": run_id, **settings, "set": which, "note": notes,
           "per_run": per_run, "score": score, "cost": cost, "results": results}
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / f"{run_id}.json").write_text(json.dumps(run, indent=1, default=repr), encoding="utf-8")
    append_log(root, [now.strftime("%Y-%m-%d"), settings["commit"], settings["seam"], settings["eval_set"],
                      settings["model"], settings["provider"], settings["split"], which, settings["k"],
                      f"{score:.2f}", spread(per_run), paired, fmt_cost(results), money(cost),
                      "-" if spent is None else money(spent), notes or "-"])
    return run_id


def emit(report: list[str]) -> None:
    try:
        print("\n".join(report))
    except (BrokenPipeError, UnicodeEncodeError):
        pass  # the run and the log row are already on disk


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one seam's evals (edd skill).")
    parser.add_argument("seam", nargs="?", help="directory name under the evals root")
    parser.add_argument("--agree-budget", type=float, default=None, metavar="DOLLARS",
                        help="run nothing: record the spending budget the user agreed for this ticket")
    parser.add_argument("--check", action="store_true",
                        help="run nothing paid: check the eval set and the adapter, show the cost estimate")
    parser.add_argument("--target", type=float, default=None,
                        help=f"the target, in place of the one in the seam's {TARGET_FILE}: the core set must "
                             f"reach it before the extended set runs")
    parser.add_argument("--split", default="dev", choices=["dev", "heldout"])
    parser.add_argument("--k", type=int, default=3, help="runs per case, odd")
    parser.add_argument("--workers", type=int, default=1, help="cases run in parallel (1 for local CPU models)")
    parser.add_argument("--note", default="", help="the one change under test")
    parser.add_argument("--model", default=None, help="the model to call, in place of the adapter's MODEL")
    parser.add_argument("--provider", default=None, help="in place of the adapter's PROVIDER")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent), help="evals root directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.agree_budget is not None:
        return agree_budget(root, args.agree_budget, args.note)
    if not args.seam:
        parser.error("the seam is required")
    seam_dir = root / args.seam
    runs_dir = seam_dir / "runs"
    if args.k % 2 == 0:
        sys.exit("use an odd k, so a case's majority is never a tie")
    eval_set = eval_set_path(seam_dir)
    declared = read_target(seam_dir)
    target = declared if args.target is None else args.target
    if target is None and not args.check:
        sys.exit(f"no target: write it in {seam_dir / TARGET_FILE}, on a line \"- Target: 0.80\"; "
                 f"it decides whether the extended set runs")

    sys.path[:0] = [str(seam_dir), str(root)]  # graders can import judge.py from the evals root
    system = load_module(seam_dir / "system.py", f"{args.seam}_system")
    grader = load_module(seam_dir / "grader.py", f"{args.seam}_grader")
    core, rest = load_cases(eval_set, args.split)
    # --model and --provider are handed to the adapter, which reads its constants when it calls:
    # the model logged is the model called.
    if args.model:
        system.MODEL = args.model
    if args.provider:
        system.PROVIDER = args.provider
    model = getattr(system, "MODEL", "?")
    provider = getattr(system, "PROVIDER", "?")
    commit = git_commit(root)
    k = args.k
    settings = {"seam": args.seam, "eval_set": eval_set.name, "split": args.split, "k": k,
                "model": model, "provider": provider, "commit": commit,
                "cases_hash": eval_set_hash(eval_set), "grader_hash": file_hash(seam_dir / "grader.py")}

    # Free checks before any paid call: the eval set has been read and checked, the adapter and the
    # grader import. The estimate prices every call at the last measured cost of this model.
    per_call = cost_per_call(system, runs_dir, model)
    if per_call is None:
        sys.exit(f"no cost estimate for {model}: declare COST_PER_CASE in system.py, in dollars per call "
                 f"(0 for a free local model)")
    spending = read_spending(root)
    core_estimate, rest_estimate = per_call * k * len(core), per_call * k * len(rest)
    if args.check:
        print(f"{args.seam} | {eval_set.name} | {args.split}: {len(core)} core cases, {len(rest)} more in the "
              f"extended set; nothing called")
        print(f"estimate at k={k}: core set {money(core_estimate)}, extended set "
              f"{money(core_estimate + rest_estimate)} in all ({money(per_call)} per call)")
        print(fmt_total(spending))
        return 0
    why_not = refusal(spending, core_estimate + rest_estimate,
                      f"the core and extended sets ({len(core) + len(rest)} cases, k={k})")
    if why_not:
        sys.exit(why_not)

    # The core set first: a change that fails it is rejected without a call spent on the rest.
    core_results = run_cases(core, system, grader, k, args.workers, per_call)
    core_score, core_per_run = scores(core_results, k)
    core_cost = sum(r["cost"] for r in core_results)
    spent_before = spending["spent"] if spending else 0.0
    core_run = save_run(root, runs_dir, settings, "core", core_results, core_score, core_per_run, args.note,
                        spent=spent_before + core_cost if spending else None)
    record_spending(root, spending, core_run, core_cost)
    report = [f"{args.seam} | {eval_set.name} | {args.split} | k={k} | {model} ({provider}) | {commit}",
              f"core set: {core_score:.2f} (spread {spread(core_per_run)}) over {len(core_results)} cases",
              f"cost {money(core_cost)}; {fmt_total(spending)}"]
    if args.target is not None and declared is not None and args.target != declared:
        report.append(f"target {target:.2f} from --target; {TARGET_FILE} says {declared:.2f}")
    if core_score < target:
        report.append(f"target {target:.2f}: not met on the core set; the extended set "
                      f"({len(rest)} more cases) does not run")
        report.append(f"run saved: {runs_dir / (core_run + '.json')}")
        emit(report)
        return 1

    # The extended set: the whole split, reusing the core results already paid for. Checked again,
    # because the core set may have cost more than its estimate.
    why_not = refusal(spending, rest_estimate, f"the extended set ({len(rest)} more cases, k={k})")
    if why_not:
        emit(report)
        sys.exit(why_not)
    rest_results = run_cases(rest, system, grader, k, args.workers, per_call)
    rest_cost = sum(r["cost"] for r in rest_results)
    results = core_results + rest_results
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

    # Judge against the target and this model's best result, paired case by case with its run.
    notes = [args.note] if args.note else []
    paired = "-"
    best, discarded = load_best(seam_dir, settings)
    if discarded:
        report.append(discarded)
        notes.append("best results discarded")
    of_split = best["splits"].setdefault(args.split, {})
    mine = of_split.get(model)
    for other, entry in sorted(of_split.items()):
        report.append(("best result: " if other == model else "best result of another model: ")
                      + fmt_best(other, entry, commit))
    if mine is None:
        report.append(f"no best result for {model} on {args.split} yet")
    elif (runs_dir / f"{mine['run_id']}.json").exists():
        before_run = json.loads((runs_dir / f"{mine['run_id']}.json").read_text(encoding="utf-8"))
        before = {r["id"]: r["passed"] for r in before_run["results"]}
        common = [r for r in results if r["id"] in before]
        gains = [r["id"] for r in common if r["passed"] and not before[r["id"]]]
        losses = [r["id"] for r in common if not r["passed"] and before[r["id"]]]
        p = sign_test(len(gains), len(losses))
        paired = f"+{len(gains)}/-{len(losses)} (p={p:.2f})"
        report.append(f"vs best result {mine['run_id']}: {paired} over {len(common)} cases")
        if gains:
            report.append(f"  gains: {', '.join(gains)}")
        if losses:
            report.append(f"  losses: {', '.join(losses)} (keeping this change accepts them)")
            notes.append(f"losses: {', '.join(losses)}")
    report.extend(verdict(score, per_run, target, mine))

    run_id = save_run(root, runs_dir, settings, "extended", results, score, per_run, "; ".join(notes),
                      paired=paired, cost=rest_cost, spent=spending["spent"] + rest_cost if spending else None)
    record_spending(root, spending, run_id, rest_cost)
    report.append(f"cost {money(rest_cost)} for the rest of the set; {fmt_total(spending)}")
    if score < target:
        report.append("below the target: the run is recorded, and is not kept as a best result")
    elif mine is None or score > mine["score"]:
        of_split[model] = {"score": score, "per_run": per_run, "code": commit, "run_id": run_id}
        report.append(f"new best result for {model} on {args.split}")
    (seam_dir / "best.json").write_text(json.dumps(best, indent=1), encoding="utf-8")
    report.append(f"run saved: {runs_dir / (run_id + '.json')}")
    emit(report)
    return 0 if score >= target else 1


if __name__ == "__main__":
    sys.exit(main())
