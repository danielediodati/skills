"""Adapter for triage_ticket: one case through the seam, the model called with `claude -p`.

The seam is the copy in this directory (`seam.py`, `test.py`, `charter.md`), taken from
`trials/seams/triage_ticket/` and `trials/charters/`: those are the fixtures of the silent drift
trials and stay as their protocol found them.

The model is Claude Code in print mode with its own system prompt replaced and no tools, so the
seam's prompt is all the model reads. The cost of a call is what Claude Code reports for it
(`total_cost_usd`): on a subscription it is the price the call would have had, not a charge.

EDD_MODEL names the model, and so does the runner's `--model`, which sets MODEL before the first call.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from datetime import datetime
from pathlib import Path

from seam import triage_ticket

MODEL = os.environ.get("EDD_MODEL", "claude-haiku-5-5")
PROVIDER = "claude-code"
COST_PER_CASE = 0.005  # a guess until the first run measures it

SYSTEM_PROMPT = "You are a helpful assistant."
TIMEOUT_SECONDS = 120
OUTPUTS = Path(__file__).resolve().parent / "runs" / "outputs.jsonl"
_outputs_lock = threading.Lock()


def run(case_input):
    calls = []

    def model(prompt):
        claude = shutil.which("claude")
        if claude is None:
            raise RuntimeError("claude is not on PATH")
        completed = subprocess.run(
            [claude, "-p", "--safe-mode", "--no-session-persistence",
             "--output-format", "json", "--tools", "", "--system-prompt", SYSTEM_PROMPT,
             "--model", MODEL],
            input=prompt,
            cwd=tempfile.gettempdir(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=TIMEOUT_SECONDS,
        )
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(f"claude exited {completed.returncode} with no JSON: "
                               f"{completed.stderr[-300:]}") from None
        calls.append(result)
        if result.get("is_error"):
            raise RuntimeError(str(result.get("result"))[:300])
        return result["result"]

    output = triage_ticket(case_input, model)
    usage = [call.get("usage") or {} for call in calls]
    # The runner keeps each run's output; the model's raw answers are kept here.
    with _outputs_lock, OUTPUTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": datetime.now().isoformat(timespec="seconds"), "model": MODEL,
                            "subject": case_input.get("subject"), "output": output,
                            "answers": [call.get("result") for call in calls]}, ensure_ascii=False) + "\n")
    return {
        "output": output,
        "tokens": sum(u.get("input_tokens", 0) + u.get("output_tokens", 0)
                      + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                      for u in usage),
        "cost": sum(call.get("total_cost_usd") or 0.0 for call in calls),
    }
