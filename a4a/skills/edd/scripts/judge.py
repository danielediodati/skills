"""Model judge for the edd skill (GRADERS.md, rung 4). Standard library only.

Binary criteria, each answered yes or no with a quoted span of the output. A "yes" whose
quote does not occur in the output counts as "no": the evidence is checked, not trusted.

Works with any OpenAI-compatible chat endpoint, configured by environment variables:

    EDD_JUDGE_MODEL     required, e.g. "llama-3.3-70b-versatile" or "qwen3.5:9b"
    EDD_JUDGE_BASE_URL  default http://localhost:11434/v1 (Ollama); Groq: https://api.groq.com/openai/v1
    EDD_JUDGE_API_KEY   needed by hosted endpoints (Groq, OpenRouter), not by Ollama

The judge must not share the model and prompt of the system under test (tautological grader).

    from judge import judge
    verdicts = judge(rubric=case["rubric"], output=result["output"], context=case["input"])
    passed = all(v["pass"] for v in verdicts)
"""

from __future__ import annotations

import json
import os
import re
import urllib.request

PROMPT = """You grade one output of an AI system against a rubric.
For each criterion, answer "yes" or "no" and quote the exact span of the OUTPUT that supports the answer.
A criterion you cannot support with a quote copied from the OUTPUT is "no".
Reply with JSON only, criteria in the given order:
{"criteria": [{"criterion": "...", "answer": "yes", "quote": "..."}]}

CONTEXT (what the system received):
<<CONTEXT>>

OUTPUT:
<<OUTPUT>>

RUBRIC:
<<RUBRIC>>"""


def _normalise(text: str) -> str:
    """Lowercase and collapse whitespace, so quote matching ignores formatting."""
    return " ".join(str(text).lower().split())


def _chat(prompt: str, model: str, base_url: str, api_key: str | None, timeout: float) -> str:
    """One deterministic chat completion against an OpenAI-compatible endpoint."""
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", data=body, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())["choices"][0]["message"]["content"]


def parse_verdicts(reply: str, rubric: list[str], output: str) -> list[dict]:
    """Turn the judge's reply into one verdict per rubric criterion, verifying each quote."""
    items: list[dict] = []
    match = re.search(r"\{.*\}", reply, re.DOTALL)  # tolerate prose or code fences around the JSON
    if match:
        try:
            items = json.loads(match.group(0)).get("criteria", [])
        except (json.JSONDecodeError, AttributeError):
            items = []
    by_text = {_normalise(i.get("criterion", "")): i for i in items if isinstance(i, dict)}
    haystack = _normalise(output)
    verdicts = []
    for index, criterion in enumerate(rubric):
        # Match by criterion text first; fall back to position when the judge paraphrased it.
        item = by_text.get(_normalise(criterion))
        if item is None and index < len(items) and isinstance(items[index], dict):
            item = items[index]
        item = item or {}
        said_yes = str(item.get("answer", "")).strip().lower() == "yes"
        quote = str(item.get("quote") or "").strip()
        quote_found = bool(quote) and _normalise(quote) in haystack
        verdicts.append({
            "criterion": criterion,
            "pass": said_yes and quote_found,
            "answer": "yes" if said_yes else "no",
            "quote": quote,
            "quote_found": quote_found,
            "parsed": bool(item),
        })
    return verdicts


def judge(rubric: list[str], output, context=None, model: str | None = None,
          base_url: str | None = None, api_key: str | None = None, timeout: float = 120) -> list[dict]:
    """Grade `output` against binary `rubric` criteria. Returns one verdict dict per criterion."""
    model = model or os.environ.get("EDD_JUDGE_MODEL")
    if not model:
        raise RuntimeError("set EDD_JUDGE_MODEL (a different model from the system under test)")
    base_url = base_url or os.environ.get("EDD_JUDGE_BASE_URL", "http://localhost:11434/v1")
    api_key = api_key or os.environ.get("EDD_JUDGE_API_KEY")
    output_text = output if isinstance(output, str) else json.dumps(output, ensure_ascii=False, indent=1)
    context_text = context if isinstance(context, str) or context is None else json.dumps(context, ensure_ascii=False)
    prompt = (PROMPT.replace("<<CONTEXT>>", context_text or "(none)")
                    .replace("<<OUTPUT>>", output_text)
                    .replace("<<RUBRIC>>", "\n".join(f"{i + 1}. {c}" for i, c in enumerate(rubric))))
    reply = _chat(prompt, model, base_url, api_key, timeout)
    return parse_verdicts(reply, rubric, output_text)
