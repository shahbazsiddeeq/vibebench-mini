#!/usr/bin/env python3
"""
Google Gemini agent for CodeAssay.
Reads task description + tests, prompts a model, and writes src/solution.py.

Env:
  GOOGLE_API_KEY            (required)
  GEMINI_MODEL              (default: gemini-2.5-flash)
  GEMINI_TIMEOUT_S          (optional, default 60)
  GEMINI_MAX_OUTPUT_TOKENS  (optional, default 1024)
  GEMINI_TEMPERATURE        (optional, default 0)
  AGENT_PROMPT_VARIANT      (optional: "standard" | "secure", default "standard")
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import google.generativeai as genai

SYSTEM_STANDARD = (
    "You are a careful Python developer. "
    "Write a single self-contained Python module at `src/solution.py` that satisfies the tests. "
    "Only output code. Use standard library only."
)

SYSTEM_SECURE = (
    "You are a careful, security-conscious Python developer. "
    "Write a single self-contained Python module at `src/solution.py` that satisfies the tests. "
    "Only output code. Use standard library only. "
    "Prioritize security: validate all inputs, avoid eval/exec, use the secrets module for "
    "randomness, sanitize external data, and handle errors without exposing internals."
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


def read_task(task_dir: Path) -> tuple[str, str, str]:
    title = ""
    desc = ""
    yaml_p = task_dir / "task.yaml"
    if yaml_p.exists():
        txt = yaml_p.read_text(encoding="utf-8")
        m1 = re.search(r"title:\s*(.+)", txt)
        m2 = re.search(r"description:\s*(.+)", txt, re.S)
        title = (m1.group(1).strip() if m1 else "").strip("\"' ")
        desc = (m2.group(1).strip() if m2 else "").strip()
    test_p = sorted((task_dir / "tests_public").glob("test_*.py"))[0]
    test_text = test_p.read_text(encoding="utf-8")
    excerpt = "\n".join(test_text.splitlines()[:80])
    return title, desc, excerpt


def build_prompt(task_dir: Path) -> str:
    title, desc, test_excerpt = read_task(task_dir)
    return PROMPT_TMPL.format(title=title, desc=desc, test_excerpt=test_excerpt)


def run_quick_pytest(ws_task: Path) -> tuple[bool, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ws_task)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "tests_public", "-x", "--maxfail=1"],
            cwd=str(ws_task),
            env=env,
            capture_output=True,
            text=True,
            timeout=float(os.getenv("PYTEST_TIMEOUT_S", "60")),
        )
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT: test execution exceeded limit]"
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out


def summarize_fail(output: str, max_chars: int = 1200) -> str:
    lines = output.strip().splitlines()[-80:]
    return "\n".join(lines)[-max_chars:]


def load_ledger(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"input_tokens": 0, "output_tokens": 0, "requests": 0}


def save_ledger(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--tests", required=True)
    ap.add_argument("--cache", default=None)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--repair-once", action="store_true")
    ap.add_argument(
        "--prompt-variant", default="standard", choices=["standard", "secure"]
    )
    args = ap.parse_args()

    task_dir = Path(args.task)
    dst = task_dir / "src" / "solution.py"
    dst.parent.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    genai.configure(api_key=api_key)

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    timeout = float(os.getenv("GEMINI_TIMEOUT_S", "60"))
    max_out = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "1024"))
    temperature = float(os.getenv("GEMINI_TEMPERATURE", "0"))
    variant = args.prompt_variant
    system = SYSTEM_SECURE if variant == "secure" else SYSTEM_STANDARD

    # ledger
    if args.cache:
        run_root = Path(args.cache).parent
    else:
        run_root = task_dir.parents[3] if len(task_dir.parents) >= 4 else task_dir
    ledger_path = run_root / "cost_ledger.json"
    budget_tokens = int(os.getenv("GEMINI_TOKEN_BUDGET", "500000"))
    ledger = load_ledger(ledger_path)

    def over_budget() -> bool:
        return (
            ledger.get("input_tokens", 0) + ledger.get("output_tokens", 0)
        ) >= budget_tokens

    cache_path = None
    if args.cache:
        Path(args.cache).mkdir(parents=True, exist_ok=True)
        cache_path = Path(args.cache) / f"{task_dir.name}__{model_name}__{variant}.py"

    if over_budget():
        if cache_path and cache_path.exists() and not args.no_cache:
            dst.write_text(cache_path.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            dst.write_text("def solve(*a, **k):\n    return None\n", encoding="utf-8")
        return

    gen_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_out,
    )
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system,
        generation_config=gen_config,
    )

    def generate(prompt: str) -> str:
        for attempt in range(3):
            try:
                resp = model.generate_content(
                    prompt, request_options={"timeout": timeout}
                )
                ledger["requests"] = ledger.get("requests", 0) + 1
                u = getattr(resp, "usage_metadata", None)
                if u:
                    ledger["input_tokens"] = ledger.get("input_tokens", 0) + getattr(
                        u, "prompt_token_count", 0
                    )
                    ledger["output_tokens"] = ledger.get("output_tokens", 0) + getattr(
                        u, "candidates_token_count", 0
                    )
                save_ledger(ledger_path, ledger)
                text = resp.text if hasattr(resp, "text") else ""
                return extract_code(text)
            except Exception as e:
                msg = str(e).lower()
                if "quota" in msg or "rate" in msg or "429" in msg:
                    time.sleep(2**attempt * 5)
                else:
                    print(f"[gemini] error: {e}", file=sys.stderr)
                    break
        return ""

    # attempt 1
    if cache_path and cache_path.exists() and not args.no_cache:
        code = cache_path.read_text(encoding="utf-8").strip()
    else:
        code = generate(build_prompt(task_dir))
        if not code:
            code = "def solve(*args, **kwargs):\n    return None\n"
        if cache_path:
            cache_path.write_text(code + "\n", encoding="utf-8")
    dst.write_text(code + "\n", encoding="utf-8")

    # repair-once
    passed, out = run_quick_pytest(task_dir)
    if passed or not args.repair_once or over_budget():
        return

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


if __name__ == "__main__":
    main()
