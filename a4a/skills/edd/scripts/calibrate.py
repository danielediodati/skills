#!/usr/bin/env python3
"""Calibrate the model judge against your own labels (edd skill, GRADERS.md). Standard library only.

    python evals/calibrate.py planner
    python evals/calibrate.py planner --threshold 0.85

Reads <seam>/calibration.jsonl, one output you labelled yourself per line:

    {"id": "cal-07", "input": {...}, "output": "...", "rubric": ["c1", "c2"], "human": [true, false]}

For every criterion it reports the judge's agreement on your pass labels and on your fail labels,
separately: raw agreement hides a judge that says yes to everything. Both must reach the
threshold before the judge grades anything that decides a change. Appends a calibration row to
log.md and exits 1 when a criterion falls short. The judge is configured as in judge.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True  # no __pycache__ in evals/: it would mark the tree dirty

from judge import judge  # noqa: E402  (same directory)
from run_evals import append_log, git_commit  # noqa: E402


def agreement(labels: list[tuple[bool, bool]]) -> dict:
    """Agreement on human-pass and human-fail labels, from (human, judge) pairs of one criterion."""
    on_pass = [j for h, j in labels if h]
    on_fail = [j for h, j in labels if not h]
    return {
        "n_pass": len(on_pass),
        "n_fail": len(on_fail),
        "pass_agree": sum(on_pass) / len(on_pass) if on_pass else None,
        "fail_agree": sum(not j for j in on_fail) / len(on_fail) if on_fail else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrate the edd model judge on your labels.")
    parser.add_argument("seam")
    parser.add_argument("--threshold", type=float, default=0.85)
    parser.add_argument("--root", default=str(ROOT), help="evals root directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    path = root / args.seam / "calibration.jsonl"
    items = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    pairs: dict[str, list[tuple[bool, bool]]] = defaultdict(list)
    disagreements = []
    for item in items:
        if len(item["human"]) != len(item["rubric"]):
            sys.exit(f"{item['id']}: 'human' must have one label per rubric criterion")
        verdicts = judge(rubric=item["rubric"], output=item["output"], context=item.get("input"))
        for criterion, human, verdict in zip(item["rubric"], item["human"], verdicts):
            pairs[criterion].append((bool(human), verdict["pass"]))
            if bool(human) != verdict["pass"]:
                disagreements.append((item["id"], criterion, human, verdict))

    ok, summary = True, []
    print(f"judge {os.environ.get('EDD_JUDGE_MODEL')} on {len(items)} labelled outputs, threshold {args.threshold}")
    for criterion, labels in pairs.items():
        a = agreement(labels)
        rates = [r for r in (a["pass_agree"], a["fail_agree"]) if r is not None]
        good = len(rates) == 2 and min(rates) >= args.threshold
        ok = ok and good
        fmt = lambda r: "n/a" if r is None else f"{r:.2f}"
        print(f"- {criterion}: pass {fmt(a['pass_agree'])} ({a['n_pass']}), "
              f"fail {fmt(a['fail_agree'])} ({a['n_fail']}) {'ok' if good else 'BELOW'}")
        if a["n_fail"] < len(labels) / 3:
            print(f"  fewer than a third of the labels fail: add failing examples before trusting it")
        summary.append(f"{criterion[:40]} {fmt(a['pass_agree'])}/{fmt(a['fail_agree'])}")

    for item_id, criterion, human, verdict in disagreements:
        print(f"  disagree {item_id} | {criterion} | you: {'pass' if human else 'fail'} | "
              f"judge: {verdict['answer']} quote={verdict['quote'][:60]!r} found={verdict['quote_found']}")

    all_rates = [r for labels in pairs.values() for r in agreement(labels).values()
                 if isinstance(r, float)]
    append_log(root, [datetime.now().strftime("%Y-%m-%d"), git_commit(root), args.seam, "calibration.jsonl",
                      os.environ.get("EDD_JUDGE_MODEL", "?"),
                      os.environ.get("EDD_JUDGE_BASE_URL", "http://localhost:11434/v1"),
                      "calibration", "calibration", 1,
                      f"{min(all_rates):.2f}" if all_rates else "-", "-", "-", "-", "-", "-",
                      "pass/fail agreement: " + "; ".join(summary)])
    print("calibrated" if ok else "not calibrated: rewrite or split the criteria marked BELOW")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
