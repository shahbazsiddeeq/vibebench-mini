#!/usr/bin/env python3
"""
Anthropic Claude agent for CodeAssay.
Reads task description + tests, prompts a model, and writes src/solution.py.

Instrumentation (revision R2):
  * attempt 1 is preserved at <cache>/attempt1/<key>.py and is never overwritten
    by the repair attempt;
  * one JSON object per API call is appended to $RUN_ROOT/events.jsonl with the
    stop reason, truncation flag, token usage, message id, wall time and any
    exception text;
  * the repair decision (public-test outcome + reason for not repairing) is
    logged as its own event;
  * $RUN_ROOT/runinfo.json records the model settings actually used.

The agent NEVER reads tests_hidden; grading of attempt 1 happens later, in the
audit script.

Env:
  ANTHROPIC_API_KEY        (required)
  CLAUDE_MODEL             (default: claude-haiku-4-5-20251001)
  CLAUDE_TIMEOUT_S         (optional, default 60)
  CLAUDE_MAX_OUTPUT_TOKENS (optional, default 1024)
  CLAUDE_TEMPERATURE       (optional, default 0; omitted for 5-gen models)
  CLAUDE_TOKEN_BUDGET      (optional, default 500000)
  AGENT_PROMPT_VARIANT     (optional: "standard" | "secure", default "standard")
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

import anthropic

PROVIDER = "anthropic"
ENDPOINT = "messages.create"

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
    # PUBLIC split only; the model never sees tests_hidden
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
    ap.add_argument(
        "--model",
        default=None,
        help="Override CLAUDE_MODEL env var (e.g. claude-3-5-sonnet-20241022)",
    )
    args = ap.parse_args()

    task_dir = Path(args.task)
    task_id = task_dir.name
    dst = task_dir / "src" / "solution.py"
    dst.parent.mkdir(parents=True, exist_ok=True)

    model = args.model or os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
    timeout = float(os.getenv("CLAUDE_TIMEOUT_S", "60"))
    max_out = int(os.getenv("CLAUDE_MAX_OUTPUT_TOKENS", "1024"))
    temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0"))
    variant = args.prompt_variant
    system = SYSTEM_SECURE if variant == "secure" else SYSTEM_STANDARD
    # Claude 5-generation models deprecate `temperature`; it is omitted for them
    # and they then run at the provider default.
    sends_temperature = not any(
        s in model for s in ("-sonnet-5", "-opus-5", "-haiku-5")
    )

    # ledger / run root
    run_root_env = os.getenv("RUN_ROOT")
    if run_root_env:
        run_root = Path(run_root_env)
    elif args.cache:
        run_root = Path(args.cache).parent
    else:
        run_root = task_dir.parents[3] if len(task_dir.parents) >= 4 else task_dir
    ledger_path = run_root / "cost_ledger.json"
    budget_tokens = int(os.getenv("CLAUDE_TOKEN_BUDGET", "500000"))
    ledger = load_ledger(ledger_path)

    write_runinfo(
        run_root,
        {
            "run": run_root.name,
            "provider": PROVIDER,
            "endpoint": ENDPOINT,
            "model": model,
            "prompt_variant": variant,
            "temperature": temperature if sends_temperature else "provider default",
            "max_output_tokens": max_out,
            "token_budget": budget_tokens,
            "timeout_s": timeout,
            "repair_once": bool(args.repair_once),
            "cache_enabled": not args.no_cache,
            "sdk": "anthropic",
            "sdk_version": getattr(anthropic, "__version__", "unknown"),
            "python": sys.version.split()[0],
            "run_started_utc": utc_now(),
        },
    )

    def over_budget() -> bool:
        return (
            ledger.get("input_tokens", 0) + ledger.get("output_tokens", 0)
        ) >= budget_tokens

    # cache key includes model + variant
    cache_path = None
    key = f"{task_id}__{model}__{variant}.py"
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
            "prompt_variant": variant,
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
        else:
            dst.write_text("def solve(*a, **k):\n    return None\n", encoding="utf-8")
        return

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate(prompt: str, attempt: int) -> str:
        for try_i in range(3):
            kwargs = dict(
                model=model,
                max_tokens=max_out,
                system=system,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout,
            )
            if sends_temperature:
                kwargs["temperature"] = temperature

            ev = base_event(
                event="api_call",
                attempt=attempt,
                retry=try_i,
                max_output_tokens=max_out,
                temperature=temperature if sends_temperature else "provider default",
            )
            t0 = time.monotonic()
            try:
                resp = client.messages.create(**kwargs)
            except anthropic.RateLimitError as exc:
                ev.update(
                    {
                        "event": "api_error",
                        "wall_s": round(time.monotonic() - t0, 3),
                        "response_id": None,
                        "finish_reason": None,
                        "stop_reason": None,
                        "truncated": None,
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                        "cached_tokens": None,
                        "cache_creation_input_tokens": None,
                        "error_type": type(exc).__name__,
                        "error": str(exc)[:2000],
                        "will_retry": try_i < 2,
                        "empty_code": True,
                        "code_chars": 0,
                    }
                )
                log_event(run_root, ev)
                time.sleep(2**try_i * 5)
                continue
            except Exception as exc:
                # A provider timeout must be an event, not a dead process.
                ev.update(
                    {
                        "event": "api_error",
                        "wall_s": round(time.monotonic() - t0, 3),
                        "response_id": None,
                        "finish_reason": None,
                        "stop_reason": None,
                        "truncated": None,
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                        "cached_tokens": None,
                        "cache_creation_input_tokens": None,
                        "error_type": type(exc).__name__,
                        "error": str(exc)[:2000],
                        "will_retry": False,
                        "empty_code": True,
                        "code_chars": 0,
                    }
                )
                log_event(run_root, ev)
                print(f"[claude] error: {type(exc).__name__}: {exc}", file=sys.stderr)
                break

            wall_s = round(time.monotonic() - t0, 3)

            # ---- stop reason / truncation ----
            stop_reason = getattr(resp, "stop_reason", None)
            truncated = bool(stop_reason == "max_tokens")

            # ---- usage ----
            u = getattr(resp, "usage", None)
            in_tok = as_int(getattr(u, "input_tokens", None)) if u is not None else None
            out_tok = (
                as_int(getattr(u, "output_tokens", None)) if u is not None else None
            )
            cache_read = (
                as_int(getattr(u, "cache_read_input_tokens", None))
                if u is not None
                else None
            )
            cache_create = (
                as_int(getattr(u, "cache_creation_input_tokens", None))
                if u is not None
                else None
            )

            ledger["requests"] = ledger.get("requests", 0) + 1
            ledger["input_tokens"] = ledger.get("input_tokens", 0) + (in_tok or 0)
            ledger["output_tokens"] = ledger.get("output_tokens", 0) + (out_tok or 0)
            save_ledger(ledger_path, ledger)

            # 5-gen models return a `thinking` block before the `text` block;
            # extract only text blocks (content[0] may be empty thinking).
            text = "".join(
                getattr(b, "text", "")
                for b in (resp.content or [])
                if getattr(b, "type", "") == "text"
            )
            code = extract_code(text)

            ev.update(
                {
                    "wall_s": wall_s,
                    "response_id": getattr(resp, "id", None),
                    "stop_reason": stop_reason,
                    # surfaced under a common name so every event across
                    # providers carries a comparable finish-reason field
                    "finish_reason": stop_reason,
                    "stop_sequence": getattr(resp, "stop_sequence", None),
                    "truncated": truncated,
                    "prompt_tokens": in_tok,
                    "completion_tokens": out_tok,
                    "total_tokens": (
                        (in_tok or 0) + (out_tok or 0)
                        if (in_tok is not None or out_tok is not None)
                        else None
                    ),
                    "cached_tokens": cache_read,
                    "cache_creation_input_tokens": cache_create,
                    "error_type": None,
                    "error": None,
                    "raw_text_chars": len(text),
                    "code_chars": len(code),
                    "empty_code": not code,
                }
            )
            log_event(run_root, ev)
            return code
        return ""

    # ---------- attempt 1 ----------
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
        code = generate(build_prompt(task_dir), attempt=1)
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
