#!/usr/bin/env python3
"""
OpenAI agent for VibeBench-Mini (Responses API).
Reads task description + tests, prompts a model, and writes src/solution.py.

Env:
  OPENAI_API_KEY   (required)
  OPENAI_MODEL     (default: gpt-4o-mini)
  OPENAI_TIMEOUT_S (optional, default 60)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
from functools import cache
from pathlib import Path

from openai import OpenAI  # pip install openai>=1.0

SYSTEM = (
    "You are a careful Python developer. "
    "Write a single self-contained Python module at `src/solution.py` that satisfies the tests. "
    "Only output code. Use standard library only."
)

PROMPT_TMPL = """\
Task title: {title}

Task description:
{desc}

Unit test (excerpt):
{test_excerpt}

Implement the function(s) imported in the test from `src.solution`.
Return correct types. Avoid I/O and prints.
"""


def sniff_func_name(test_text: str) -> str | None:
    m = re.search(
        r"from\s+src\.solution\s+import\s+([A-Za-z_][A-Za-z0-9_]*)", test_text
    )
    return m.group(1) if m else None


def read_task(task_dir: Path) -> tuple[str, str, str]:
    # title/desc
    title = ""
    desc = ""
    yaml_p = task_dir / "task.yaml"
    if yaml_p.exists():
        txt = yaml_p.read_text(encoding="utf-8")
        m1 = re.search(r"title:\s*(.+)", txt)
        m2 = re.search(r"description:\s*(.+)", txt, re.S)
        title = (m1.group(1).strip() if m1 else "").strip("\"' ")
        desc = (m2.group(1).strip() if m2 else "").strip()
    # test
    test_p = sorted((task_dir / "tests").glob("test_*.py"))[0]
    test_text = test_p.read_text(encoding="utf-8")
    # excerpt (trim to keep prompt compact)
    excerpt = "\n".join(test_text.splitlines()[:80])
    return title, desc, excerpt


def build_prompt(task_dir: Path) -> str:
    title, desc, test_excerpt = read_task(task_dir)
    return PROMPT_TMPL.format(title=title, desc=desc, test_excerpt=test_excerpt)


def run_quick_pytest(ws_task: Path) -> tuple[bool, str]:
    """Run pytest once for this task; return (passed, combined_output)."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ws_task)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests", "-x", "--maxfail=1"],
        cwd=str(ws_task),
        env=env,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out


def summarize_fail(output: str, max_chars: int = 1200) -> str:
    """Trim pytest output to a compact, useful summary for the model."""
    # Keep last ~80 lines; pytest puts failure at the end.
    lines = output.strip().splitlines()[-80:]
    text = "\n".join(lines)
    return text[-max_chars:]


def load_ledger(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {"input_tokens": 0, "output_tokens": 0, "requests": 0}
    return {"input_tokens": 0, "output_tokens": 0, "requests": 0}


def save_ledger(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--task", required=True, help="Workspace task dir to write into (has src/solution.py)")
#     ap.add_argument("--tests", required=True, help="Original tests path (unused; provided by harness)")
#     args = ap.parse_args()

#     task_dir = Path(args.task)
#     prompt = build_prompt(task_dir)

#     client = OpenAI()
#     model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#     timeout = float(os.getenv("OPENAI_TIMEOUT_S", "60"))

#     # Call Responses API (preferred in 2025)
#     # Ref: openai-python README & docs. response.output_text contains the text. :contentReference[oaicite:1]{index=1}
#     response = client.responses.create(
#         model=model,
#         input=[
#             {"role": "system", "content": SYSTEM},
#             {"role": "user", "content": prompt},
#         ],
#         timeout=timeout,
#     )
#     code = response.output_text or ""

#     # Minimal guard: extract code block if user content got wrapped
#     m = re.search(r"```(?:python)?\n(.*?)```", code, re.S)
#     if m:
#         code = m.group(1).strip()

#     dst = task_dir / "src" / "solution.py"
#     dst.parent.mkdir(parents=True, exist_ok=True)
#     if not code.strip():
#         # fallback stub so tests import cleanly
#         code = "def solve(*args, **kwargs):\n    return None\n"
#     dst.write_text(code.strip() + "\n", encoding="utf-8")

# if __name__ == "__main__":
#     main()


# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--task", required=True, help="Workspace task dir to write into (has src/solution.py)")
#     ap.add_argument("--tests", required=True, help="Original tests path (unused; provided by harness)")
#     ap.add_argument("--cache", default=None, help="Cache dir for generated solutions (optional)")
#     ap.add_argument("--no-cache", action="store_true", help="Disable cache")
#     args = ap.parse_args()

#     task_dir = Path(args.task)
#     dst = task_dir / "src" / "solution.py"
#     dst.parent.mkdir(parents=True, exist_ok=True)

#     # simple cache by task name
#     cache_path = None
#     if args.cache:
#         Path(args.cache).mkdir(parents=True, exist_ok=True)
#         cache_path = Path(args.cache) / f"{task_dir.name}.py"

#     if cache_path and cache_path.exists() and not args.no_cache:
#         dst.write_text(cache_path.read_text(encoding="utf-8"), encoding="utf-8")
#         return  # cache hit

#     prompt = build_prompt(task_dir)

#     client = OpenAI()
#     model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#     timeout = float(os.getenv("OPENAI_TIMEOUT_S", "60"))

#     response = client.responses.create(
#         model=model,
#         input=[
#             {"role": "system", "content": SYSTEM},
#             {"role": "user", "content": prompt},
#         ],
#         timeout=timeout,
#     )
#     code = response.output_text or ""

#     m = re.search(r"```(?:python)?\n(.*?)```", code, re.S)
#     if m:
#         code = m.group(1).strip()
#     if not code.strip():
#         code = "def solve(*args, **kwargs):\n    return None\n"

#     dst.write_text(code.strip() + "\n", encoding="utf-8")
#     if cache_path:
#         cache_path.write_text(code.strip() + "\n", encoding="utf-8")


# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument(
#         "--task", required=True, help="Workspace task dir (writes src/solution.py here)"
#     )
#     ap.add_argument("--tests", required=True, help="Original tests path (unused)")
#     ap.add_argument(
#         "--cache", default=None, help="Cache dir for generated solutions (optional)"
#     )
#     ap.add_argument("--no-cache", action="store_true", help="Disable cache")
#     ap.add_argument(
#         "--repair-once",
#         action="store_true",
#         help="If tests fail, do one repair attempt",
#     )
#     args = ap.parse_args()

#     task_dir = Path(args.task)
#     dst = task_dir / "src" / "solution.py"
#     dst.parent.mkdir(parents=True, exist_ok=True)

#     # ---------- cache (by task name) ----------
#     cache_path = None
#     if args.cache:
#         Path(args.cache).mkdir(parents=True, exist_ok=True)
#         cache_path = Path(args.cache) / f"{task_dir.name}.py"

#     if cache_path and cache_path.exists() and not args.no_cache:
#         dst.write_text(cache_path.read_text(encoding="utf-8"), encoding="utf-8")
#         # still run quick pytest to enable repair on cached code
#     else:
#         # ---------- first attempt ----------
#         prompt = build_prompt(task_dir)
#         client = OpenAI()
#         model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#         timeout = float(os.getenv("OPENAI_TIMEOUT_S", "60"))

#         resp = client.responses.create(
#             model=model,
#             input=[
#                 {"role": "system", "content": SYSTEM},
#                 {"role": "user", "content": prompt},
#             ],
#             timeout=timeout,
#         )
#         code = resp.output_text or ""
#         m = re.search(r"```(?:python)?\n(.*?)```", code, re.S)
#         if m:
#             code = m.group(1).strip()
#         if not code.strip():
#             code = "def solve(*args, **kwargs):\n    return None\n"
#         dst.write_text(code.strip() + "\n", encoding="utf-8")
#         if cache_path:
#             cache_path.write_text(code.strip() + "\n", encoding="utf-8")

#     # ---------- quick test + optional one-shot repair ----------
#     passed, out = run_quick_pytest(task_dir)
#     if passed or not args.repair - once:
#         return

#     summary = summarize_fail(out)
#     repair_prompt = textwrap.dedent(
#         f"""\
#     The code you wrote for the task failed the unit test below. Please FIX the entire module `src/solution.py`.
#     Output ONLY the full corrected Python file content.

#     --- TEST FAILURE (truncated) ---
#     {summary}
#     --- END FAILURE ---

#     Re-check types, edge cases, and avoid I/O. Keep it standard library only.
#     """
#     )

#     client = OpenAI()
#     model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#     timeout = float(os.getenv("OPENAI_TIMEOUT_S", "60"))

#     resp2 = client.responses.create(
#         model=model,
#         input=[
#             {"role": "system", "content": SYSTEM},
#             {"role": "user", "content": build_prompt(task_dir)},
#             {"role": "user", "content": repair_prompt},
#         ],
#         timeout=timeout,
#     )
#     code2 = resp2.output_text or ""
#     m2 = re.search(r"```(?:python)?\n(.*?)```", code2, re.S)
#     if m2:
#         code2 = m2.group(1).strip()
#     if code2.strip():
#         dst.write_text(code2.strip() + "\n", encoding="utf-8")
#         if cache_path:
#             cache_path.write_text(code2.strip() + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--task", required=True, help="Workspace task dir (writes src/solution.py here)"
    )
    ap.add_argument("--tests", required=True, help="Original tests path (unused)")
    ap.add_argument(
        "--cache", default=None, help="Cache dir for generated solutions (optional)"
    )
    ap.add_argument("--no-cache", action="store_true", help="Disable cache")
    ap.add_argument(
        "--repair-once",
        action="store_true",
        help="If tests fail, do one repair attempt",
    )
    args = ap.parse_args()

    task_dir = Path(args.task)
    dst = task_dir / "src" / "solution.py"
    dst.parent.mkdir(parents=True, exist_ok=True)

    # -------- settings from env (determinism + limits) --------
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    timeout = float(os.getenv("OPENAI_TIMEOUT_S", "60"))
    temperature = float(
        os.getenv("OPENAI_TEMPERATURE", "0")
    )  # 0 ⇒ most deterministic. :contentReference[oaicite:0]{index=0}
    max_out = int(
        os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "400")
    )  # cap output tokens. :contentReference[oaicite:1]{index=1}
    seed_env = os.getenv("OPENAI_SEED")  # optional; only some models honor it
    seed = int(seed_env) if seed_env and seed_env.isdigit() else None

    # -------- simple token budget (per run root) --------

    run_root_env = os.getenv("RUN_ROOT")
    if run_root_env:
        run_root = Path(run_root_env)
    elif args.cache:
        run_root = Path(args.cache).parent  # e.g., .../.agent_runs/openai-default
    else:
        run_root = task_dir.parents[3] if len(task_dir.parents) >= 4 else task_dir

    # run_root = Path(os.getenv("RUN_ROOT", task_dir.parents[3]))  # .agent_runs/<agent>

    ledger_path = run_root / "cost_ledger.json"
    budget_tokens = int(
        os.getenv("OPENAI_TOKEN_BUDGET", "200000")
    )  # total in+out tokens allowed for the run
    ledger = load_ledger(ledger_path)
    save_ledger(ledger_path, ledger)

    def over_budget() -> bool:
        return (
            ledger.get("input_tokens", 0) + ledger.get("output_tokens", 0)
        ) >= budget_tokens

    # -------- cache key includes model + temperature --------
    cache_path = None
    if args.cache:
        Path(args.cache).mkdir(parents=True, exist_ok=True)
        key = f"{task_dir.name}__{model}__t{temperature}.py"
        cache_path = Path(args.cache) / key

    # If over budget, try cache; if none, write stub and exit early
    if over_budget():
        if cache_path and cache_path.exists() and not args.no - cache:
            dst.write_text(cache_path.read_text(encoding="utf-8"), encoding="utf-8")
            return
        dst.write_text("def solve(*a, **k):\n    return None\n", encoding="utf-8")
        return

    client = OpenAI()

    def generate(prompt: str) -> str:
        # Create a response with deterministic params and safety caps. :contentReference[oaicite:2]{index=2}
        kwargs = dict(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt},
            ],
            timeout=timeout,
            temperature=temperature,
            max_output_tokens=max_out,
        )
        if seed is not None:
            kwargs["seed"] = (
                seed  # some models support seeding; if ignored, API still succeeds.
            )
        resp = client.responses.create(**kwargs)
        # track usage if present
        u = getattr(resp, "usage", None)
        # if u:
        #     ledger["input_tokens"] = ledger.get("input_tokens", 0) + getattr(u, "input_tokens", 0)
        #     ledger["output_tokens"] = ledger.get("output_tokens", 0) + getattr(u, "output_tokens", 0)
        #     ledger["requests"] = ledger.get("requests", 0) + 1
        #     save_ledger(ledger_path, ledger)

        ledger["requests"] = ledger.get("requests", 0) + 1
        if u:
            ledger["input_tokens"] = ledger.get("input_tokens", 0) + getattr(
                u, "input_tokens", 0
            )
            ledger["output_tokens"] = ledger.get("output_tokens", 0) + getattr(
                u, "output_tokens", 0
            )
        save_ledger(ledger_path, ledger)

        text = getattr(
            resp, "output_text", ""
        )  # SDK convenience prop. :contentReference[oaicite:3]{index=3}
        m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
        return (m.group(1) if m else text).strip()

    # ---------- attempt 1 (cache or fresh) ----------
    if cache_path and cache_path.exists() and not args.no - cache:
        code = cache_path.read_text(encoding="utf-8").strip()
    else:
        prompt1 = build_prompt(task_dir)
        code = generate(prompt1)
        if not code:
            code = "def solve(*args, **kwargs):\n    return None\n"
        if cache_path:
            cache_path.write_text(code + "\n", encoding="utf-8")
    dst.write_text(code + "\n", encoding="utf-8")

    # ---------- quick test + optional one-shot repair ----------
    passed, out = run_quick_pytest(task_dir)
    if passed or not args.repair_once or over_budget():
        return

    # repair with failure summary appended
    repair_prompt = textwrap.dedent(
        f"""\
    The code for this task failed the unit test below. FIX the entire module `src/solution.py`.
    Output ONLY the full corrected Python file.

    --- TRUNCATED TEST FAILURE ---
    {summarize_fail(out)}
    --- END ---
    """
    )
    code2 = generate(build_prompt(task_dir) + "\n\n" + repair_prompt)
    if code2:
        dst.write_text(code2.strip() + "\n", encoding="utf-8")
        if cache_path:
            cache_path.write_text(code2.strip() + "\n", encoding="utf-8")
