#!/usr/bin/env python3
"""
OpenAI agent for CodeAssay (Responses API).
Reads task description + tests, prompts a model, and writes src/solution.py.

Instrumentation (revision R2):
  * attempt 1 is preserved at <cache>/attempt1/<key>.py and is never overwritten
    by the repair attempt;
  * one JSON object per API call is appended to $RUN_ROOT/events.jsonl with the
    finish reason, truncation flag, token usage, response id, wall time and any
    exception text;
  * the repair decision (public-test outcome + reason for not repairing) is
    logged as its own event;
  * $RUN_ROOT/runinfo.json records the model settings actually used.

The agent NEVER reads tests_hidden; grading of attempt 1 happens later, in the
audit script.

Env:
  OPENAI_API_KEY           (required)
  OPENAI_MODEL             (default: gpt-4o-mini)
  OPENAI_TIMEOUT_S         (optional, default 60)
  OPENAI_TEMPERATURE       (optional, default 0; omitted for gpt-5* models)
  OPENAI_MAX_OUTPUT_TOKENS (optional, default 1024)
  OPENAI_TOKEN_BUDGET      (optional, default 200000)
  OPENAI_SEED              (optional)
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
from datetime import datetime, timezone
from pathlib import Path

import openai
from openai import OpenAI  # pip install openai>=1.0

PROVIDER = "openai"
ENDPOINT = "responses.create"

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


# --------------------------------------------------------------------------
# instrumentation helpers
# --------------------------------------------------------------------------
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def as_int(value) -> int | None:
    """Coerce an SDK usage field to int; None when the API did not report it."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def log_event(run_root: Path, payload: dict) -> None:
    """Append exactly one JSON object per line to $RUN_ROOT/events.jsonl."""
    try:
        run_root.mkdir(parents=True, exist_ok=True)
        line = json.dumps(payload, ensure_ascii=False, default=str) + "\n"
        with open(run_root / "events.jsonl", "a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
    except Exception as exc:  # instrumentation must never kill a paid run
        print(f"[{PROVIDER}] event-log failure: {exc}", file=sys.stderr)


def write_runinfo(run_root: Path, info: dict) -> None:
    """Write $RUN_ROOT/runinfo.json once per run (start time is preserved)."""
    try:
        run_root.mkdir(parents=True, exist_ok=True)
        path = run_root / "runinfo.json"
        started = info.get("run_started_utc")
        if path.exists():
            try:
                prev = json.loads(path.read_text(encoding="utf-8"))
                started = prev.get("run_started_utc", started)
            except Exception:
                pass
        info = dict(info, run_started_utc=started)
        path.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"[{PROVIDER}] runinfo failure: {exc}", file=sys.stderr)


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
    # test (PUBLIC split only; the model never sees tests_hidden)
    test_p = sorted((task_dir / "tests_public").glob("test_*.py"))[0]
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


def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()


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
    ap.add_argument(
        "--prompt-variant",
        default="standard",
        choices=["standard", "secure"],
        help="Prompt variant: standard or security-aware",
    )
    ap.add_argument(
        "--model",
        default=None,
        help="Override OPENAI_MODEL env var (e.g. gpt-4o, gpt-4o-mini)",
    )
    args = ap.parse_args()

    task_dir = Path(args.task)
    task_id = task_dir.name
    dst = task_dir / "src" / "solution.py"
    dst.parent.mkdir(parents=True, exist_ok=True)

    # -------- settings from env (determinism + limits) --------
    model = args.model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    timeout = float(os.getenv("OPENAI_TIMEOUT_S", "60"))
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))
    max_out = int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "1024"))
    system = SYSTEM_SECURE if args.prompt_variant == "secure" else SYSTEM_STANDARD
    seed_env = os.getenv("OPENAI_SEED")  # optional; only some models honor it
    seed = int(seed_env) if seed_env and seed_env.isdigit() else None
    # gpt-5.x (reasoning) models reject `temperature`; it is omitted for them and
    # they then run at the provider default.
    sends_temperature = not model.startswith("gpt-5")

    # -------- simple token budget (per run root) --------

    run_root_env = os.getenv("RUN_ROOT")
    if run_root_env:
        run_root = Path(run_root_env)
    elif args.cache:
        run_root = Path(args.cache).parent  # e.g., .../.agent_runs/openai-default
    else:
        run_root = task_dir.parents[3] if len(task_dir.parents) >= 4 else task_dir

    ledger_path = run_root / "cost_ledger.json"
    budget_tokens = int(
        os.getenv("OPENAI_TOKEN_BUDGET", "200000")
    )  # total in+out tokens allowed for the run
    ledger = load_ledger(ledger_path)
    save_ledger(ledger_path, ledger)

    write_runinfo(
        run_root,
        {
            "run": run_root.name,
            "provider": PROVIDER,
            "endpoint": ENDPOINT,
            "model": model,
            "prompt_variant": args.prompt_variant,
            "temperature": temperature if sends_temperature else "provider default",
            "max_output_tokens": max_out,
            "token_budget": budget_tokens,
            "timeout_s": timeout,
            "seed": seed if seed is not None else "not sent",
            "repair_once": bool(args.repair_once),
            "cache_enabled": not args.no_cache,
            "sdk": "openai",
            "sdk_version": getattr(openai, "__version__", "unknown"),
            "python": sys.version.split()[0],
            "run_started_utc": utc_now(),
        },
    )

    def over_budget() -> bool:
        return (
            ledger.get("input_tokens", 0) + ledger.get("output_tokens", 0)
        ) >= budget_tokens

    # -------- cache key includes model + temperature --------
    cache_path = None
    attempt1_path = None
    key = f"{task_id}__{model}__{args.prompt_variant}.py"
    if args.cache:
        Path(args.cache).mkdir(parents=True, exist_ok=True)
        cache_path = Path(args.cache) / key
        attempt1_path = Path(args.cache) / "attempt1" / key
    else:
        attempt1_path = run_root / "attempt1" / key

    def base_event(**extra) -> dict:
        ev = {
            "ts": utc_now(),
            "run": run_root.name,
            "task_id": task_id,
            "provider": PROVIDER,
            "endpoint": ENDPOINT,
            "model": model,
            "prompt_variant": args.prompt_variant,
        }
        ev.update(extra)
        return ev

    def save_attempt1(code: str) -> None:
        """Persist attempt 1 verbatim. Only ever written by attempt 1 itself."""
        if not attempt1_path or not code:
            return
        try:
            attempt1_path.parent.mkdir(parents=True, exist_ok=True)
            attempt1_path.write_text(code + "\n", encoding="utf-8")
        except Exception as exc:
            print(f"[{PROVIDER}] attempt1 write failure: {exc}", file=sys.stderr)

    # If over budget, try cache; if none, write stub and exit early
    if over_budget():
        used_cache = bool(cache_path and cache_path.exists() and not args.no_cache)
        log_event(
            run_root,
            base_event(
                event="budget_skip",
                attempt=1,
                reason="over_budget",
                budget_tokens=budget_tokens,
                tokens_used=ledger.get("input_tokens", 0)
                + ledger.get("output_tokens", 0),
                used_cache=used_cache,
            ),
        )
        if used_cache:
            dst.write_text(cache_path.read_text(encoding="utf-8"), encoding="utf-8")
            return
        dst.write_text("def solve(*a, **k):\n    return None\n", encoding="utf-8")
        return

    client = OpenAI()

    def generate(prompt: str, attempt: int) -> str:
        # Deterministic params and safety caps.
        kwargs = dict(
            model=model,
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            timeout=timeout,
            max_output_tokens=max_out,
        )
        if sends_temperature:
            kwargs["temperature"] = temperature
        if seed is not None:
            kwargs["seed"] = (
                seed  # some models support seeding; if ignored, API still succeeds.
            )

        ev = base_event(
            event="api_call",
            attempt=attempt,
            max_output_tokens=max_out,
            temperature=temperature if sends_temperature else "provider default",
        )
        t0 = time.monotonic()
        try:
            resp = client.responses.create(**kwargs)
        except Exception as exc:
            # A provider timeout must be an event, not a dead process.
            ev.update(
                {
                    "event": "api_error",
                    "wall_s": round(time.monotonic() - t0, 3),
                    "response_id": None,
                    "status": None,
                    "finish_reason": None,
                    "incomplete_reason": None,
                    "truncated": None,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "reasoning_tokens": None,
                    "cached_tokens": None,
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:2000],
                    "empty_code": True,
                    "code_chars": 0,
                }
            )
            log_event(run_root, ev)
            print(f"[{PROVIDER}] error: {type(exc).__name__}: {exc}", file=sys.stderr)
            return ""

        wall_s = round(time.monotonic() - t0, 3)

        # ---- finish reason / truncation (Responses API has no finish_reason) ----
        status = getattr(resp, "status", None)
        inc = getattr(resp, "incomplete_details", None)
        inc_reason = getattr(inc, "reason", None) if inc is not None else None
        truncated = bool(status == "incomplete" and inc_reason == "max_output_tokens")

        # ---- usage ----
        u = getattr(resp, "usage", None)
        otd = getattr(u, "output_tokens_details", None) if u is not None else None
        itd = getattr(u, "input_tokens_details", None) if u is not None else None
        in_tok = as_int(getattr(u, "input_tokens", None)) if u is not None else None
        out_tok = as_int(getattr(u, "output_tokens", None)) if u is not None else None
        tot_tok = as_int(getattr(u, "total_tokens", None)) if u is not None else None

        ledger["requests"] = ledger.get("requests", 0) + 1
        ledger["input_tokens"] = ledger.get("input_tokens", 0) + (in_tok or 0)
        ledger["output_tokens"] = ledger.get("output_tokens", 0) + (out_tok or 0)
        save_ledger(ledger_path, ledger)

        text = getattr(resp, "output_text", "") or ""  # SDK convenience prop
        code = extract_code(text)

        ev.update(
            {
                "wall_s": wall_s,
                "response_id": getattr(resp, "id", None),
                "status": status,
                # Responses API reports completion state via `status`; surfaced
                # as finish_reason so every event carries one comparable field.
                "finish_reason": status,
                "incomplete_reason": inc_reason,
                "truncated": truncated,
                "prompt_tokens": in_tok,
                "completion_tokens": out_tok,
                "total_tokens": tot_tok,
                "reasoning_tokens": (
                    as_int(getattr(otd, "reasoning_tokens", None))
                    if otd is not None
                    else None
                ),
                "cached_tokens": (
                    as_int(getattr(itd, "cached_tokens", None))
                    if itd is not None
                    else None
                ),
                "error_type": None,
                "error": None,
                "raw_text_chars": len(text),
                "code_chars": len(code),
                "empty_code": not code,
            }
        )
        log_event(run_root, ev)
        return code

    # ---------- attempt 1 (cache or fresh) ----------
    from_cache = bool(cache_path and cache_path.exists() and not args.no_cache)
    if from_cache:
        code = cache_path.read_text(encoding="utf-8").strip()
        log_event(
            run_root,
            base_event(
                event="cache_hit",
                attempt=1,
                cache_path=str(cache_path),
                # A cache hit may hold a repaired program from an earlier run, so
                # attempt 1 is not reconstructed from it.
                attempt1_file_present=bool(attempt1_path and attempt1_path.exists()),
            ),
        )
    else:
        prompt1 = build_prompt(task_dir)
        code = generate(prompt1, attempt=1)
        if not code:
            log_event(
                run_root,
                base_event(
                    event="no_program",
                    attempt=1,
                    reason="empty_or_failed_generation",
                ),
            )
            dst.write_text(
                "def solve(*args, **kwargs):\n    return None\n", encoding="utf-8"
            )
            return  # do not cache failed generations
        save_attempt1(code)
        if cache_path:
            cache_path.write_text(code + "\n", encoding="utf-8")
    dst.write_text(code + "\n", encoding="utf-8")

    # ---------- quick PUBLIC test + optional one-shot repair ----------
    passed, out = run_quick_pytest(task_dir)
    budget_exhausted = over_budget()
    if passed:
        no_repair_reason = "passed"
    elif not args.repair_once:
        no_repair_reason = "no_repair_flag"
    elif budget_exhausted:
        no_repair_reason = "over_budget"
    else:
        no_repair_reason = None

    log_event(
        run_root,
        base_event(
            event="repair_decision",
            attempt=1,
            attempt1_public_pass=passed,
            attempt1_from_cache=from_cache,
            repair_flag=bool(args.repair_once),
            over_budget=budget_exhausted,
            repair_attempted=no_repair_reason is None,
            no_repair_reason=no_repair_reason,
        ),
    )

    if no_repair_reason is not None:
        return

    # repair with failure summary appended (PUBLIC failure only)
    repair_prompt = textwrap.dedent(
        f"""\
    The code for this task failed the unit test below. FIX the entire module `src/solution.py`.
    Output ONLY the full corrected Python file.

    --- TRUNCATED TEST FAILURE ---
    {summarize_fail(out)}
    --- END ---
    """
    )
    code2 = generate(build_prompt(task_dir) + "\n\n" + repair_prompt, attempt=2)
    if code2:
        dst.write_text(code2.strip() + "\n", encoding="utf-8")
        if cache_path:
            cache_path.write_text(code2.strip() + "\n", encoding="utf-8")
        repaired_pass = None
        if os.getenv("VB_POST_REPAIR_PUBLIC_CHECK", "1") == "1":
            repaired_pass, _ = run_quick_pytest(task_dir)
        log_event(
            run_root,
            base_event(
                event="repair_result",
                attempt=2,
                repair_produced_code=True,
                repair_public_pass=repaired_pass,
            ),
        )
    else:
        log_event(
            run_root,
            base_event(
                event="repair_result",
                attempt=2,
                repair_produced_code=False,
                repair_public_pass=None,
            ),
        )


if __name__ == "__main__":
    main()
