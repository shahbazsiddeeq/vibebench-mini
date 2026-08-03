#!/usr/bin/env python3.12
"""Repair-pipeline audit for the instrumented r2 run.

This supersedes `scripts/verify_and_repair_audit.py` for the `.agent_runs/r2-*`
runs. The earlier script could only infer the repair pipeline from request
counts, because the cache held the final solution alone. The r2 runs preserve
the first attempt at `cache/attempt1/<key>.py` and log one JSON object per API
call and per decision to `events.jsonl`, so every quantity the audit reports
for is now measured rather than inferred.

For each configuration and task the script grades two programs against two test
suites:

    cache/attempt1/<key>.py  vs tests_public   -> initial public-test result
    cache/attempt1/<key>.py  vs tests_hidden   -> INITIAL hidden correctness
    cache/<key>.py           vs tests_public   -> final public-test result
    cache/<key>.py           vs tests_hidden   -> FINAL hidden correctness

Grading reuses `run_suite` from `verify_and_repair_audit.py`. A task directory
holds three suites whose files share the basename `test_solution.py`, so pytest
aborts with an import file mismatch when two of them are visible at once. Each
check therefore runs in a scratch directory holding the task source and exactly
one suite.

When the first attempt and the final solution are byte identical, which is the
common case because the repair only fires on a public-test failure, the two
programs are graded once and the result is reused. Pass `--no-dedupe` to grade
both copies regardless.

The grading is joined per task with `events.jsonl`, which supplies whether a
repair was attempted, the reason when it was not, and the finish reason,
truncation flag and token counts of each attempt.

Outputs:
  reports/r2_repair_audit.csv     one row per configuration per task
  reports/r2_repair_summary.md    per-configuration repair table

The script tolerates a run that is still being written. A configuration with
fewer than 185 graded tasks is reported with the tasks it has and labeled
incomplete.

Run:  python3.12 scripts/r2_repair_audit.py --workers 16
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_and_repair_audit import run_suite  # noqa: E402  (shared staging logic)

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks" / "python"
RUNS = ROOT / ".agent_runs"
REPORTS = ROOT / "reports"
SCRATCH = ROOT / ".verify_scratch" / "r2"  # .verify_scratch is already git ignored
EXPECTED_TASKS = 185

# slug -> human label used in the paper. A slug that is missing here falls back
# to the model id recorded in runinfo.json.
LABELS = {
    "gpt4omini": "GPT-4o-mini",
    "gpt4o": "GPT-4o",
    "gpt56sol": "GPT-5.6-sol",
    "haiku45": "Claude Haiku 4.5",
    "sonnet45": "Claude Sonnet 4.5",
    "sonnet5": "Claude Sonnet 5",
    "gemini25": "Gemini 2.5 Flash",
}
PROMPT_VARIANT = {"std": "standard", "sec": "secure"}
NO_REPAIR_REASONS = ["passed", "no_repair_flag", "over_budget"]


# --------------------------------------------------------------------------
# discovery
# --------------------------------------------------------------------------
def task_dirs() -> list[Path]:
    return sorted(
        t
        for t in TASKS.glob("task*")
        if (t / "tests_hidden").is_dir() and (t / "tests_public").is_dir()
    )


def discover_configs(pattern: str) -> list[dict]:
    """Return one descriptor per r2 configuration directory."""
    out = []
    for d in sorted(RUNS.glob(pattern)):
        if not (d / "cache").is_dir():
            continue
        name = d.name
        body = name[3:] if name.startswith("r2-") else name
        slug, _, prompt = body.rpartition("-")
        info = read_json(d / "runinfo.json") or {}
        out.append(
            {
                "run": name,
                "dir": d,
                "slug": slug or body,
                "prompt": prompt or "std",
                "prompt_variant": info.get(
                    "prompt_variant", PROMPT_VARIANT.get(prompt, prompt)
                ),
                "model_id": info.get("model", ""),
                "label": LABELS.get(slug, info.get("model", slug)),
                "runinfo": info,
            }
        )
    return out


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def cache_key(task: str, model_id: str, prompt_variant: str) -> str:
    """Reproduce the agents' cache key. OpenRouter ids contain a slash."""
    return f"{task}__{model_id.replace('/', '__')}__{prompt_variant}.py"


def solution_paths(cfg: dict, task: str) -> tuple[Path | None, Path | None]:
    """Return (attempt1_path, final_path), each None when absent.

    The exact key is tried first. A glob on the task prefix is the fallback, so
    a configuration whose model id was recorded differently still resolves.
    """
    cache = cfg["dir"] / "cache"
    key = cache_key(task, cfg["model_id"], cfg["prompt_variant"])

    def pick(base: Path) -> Path | None:
        p = base / key
        if p.exists():
            return p
        cands = sorted(base.glob(f"{task}__*.py")) if base.is_dir() else []
        return cands[0] if cands else None

    return pick(cache / "attempt1"), pick(cache)


# --------------------------------------------------------------------------
# events
# --------------------------------------------------------------------------
def load_events(run_dir: Path) -> dict[str, dict]:
    """Fold events.jsonl into one record per task id.

    A partially written final line is skipped, so the file can be read while the
    run is still appending to it.
    """
    per_task: dict[str, dict] = {}
    path = run_dir / "events.jsonl"
    if not path.exists():
        return per_task
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue  # truncated tail of a file still being written
            tid = ev.get("task_id")
            if not tid:
                continue
            rec = per_task.setdefault(
                tid,
                {
                    "api_calls": [],
                    "api_errors": [],
                    "repair_decision": None,
                    "repair_result": None,
                    "cache_hit": False,
                    "no_program": False,
                    "budget_skip": False,
                },
            )
            kind = ev.get("event")
            if kind == "api_call":
                # An api_call carrying an error_type is a failed call that was
                # logged through the success path by some providers.
                if ev.get("error_type"):
                    rec["api_errors"].append(ev)
                else:
                    rec["api_calls"].append(ev)
            elif kind == "api_error":
                rec["api_errors"].append(ev)
            elif kind == "repair_decision":
                rec["repair_decision"] = ev
            elif kind == "repair_result":
                rec["repair_result"] = ev
            elif kind == "cache_hit":
                rec["cache_hit"] = True
            elif kind == "no_program":
                rec["no_program"] = True
            elif kind == "budget_skip":
                rec["budget_skip"] = True
    return per_task


def last_call(rec: dict, attempt: int) -> dict:
    """The api_call whose output was used for an attempt.

    Retries append more than one event for the same attempt, so the last one
    wins.
    """
    calls = [c for c in rec.get("api_calls", []) if c.get("attempt") == attempt]
    return calls[-1] if calls else {}


def attempt_columns(call: dict, tag: str) -> dict:
    return {
        f"{tag}_finish_reason": call.get("finish_reason", ""),
        f"{tag}_truncated": call.get("truncated", ""),
        f"{tag}_prompt_tokens": call.get("prompt_tokens", ""),
        f"{tag}_completion_tokens": call.get("completion_tokens", ""),
        f"{tag}_total_tokens": call.get("total_tokens", ""),
        f"{tag}_reasoning_tokens": call.get("reasoning_tokens", ""),
        f"{tag}_cached_tokens": call.get("cached_tokens", ""),
        f"{tag}_wall_s": call.get("wall_s", ""),
    }


def reported_hidden(run_dir: Path) -> dict[str, bool]:
    """Final hidden correctness as recorded by the runner, when present."""
    path = run_dir / "results.csv"
    out: dict[str, bool] = {}
    if not path.exists():
        return out
    try:
        with path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                tid = row.get("id", "")
                if not tid or tid == "__aggregate__":
                    continue
                try:
                    out[tid] = float(row.get("correctness") or 0) >= 1.0
                except ValueError:
                    out[tid] = False
    except OSError:
        pass
    return out


# --------------------------------------------------------------------------
# grading
# --------------------------------------------------------------------------
def grade_task(job) -> dict:
    """Grade attempt 1 and the final solution against both suites."""
    cfg_run, task_dir, a1, fin, dedupe = job
    task = task_dir.name
    work = SCRATCH / cfg_run
    rec = {
        "run": cfg_run,
        "task": task,
        "attempt1_present": bool(a1),
        "final_present": bool(fin),
        "attempt1_sha256": "",
        "final_sha256": "",
        "attempt1_public_pass": "",
        "attempt1_hidden_pass": "",
        "final_public_pass": "",
        "final_hidden_pass": "",
    }
    if a1:
        rec["attempt1_sha256"] = hashlib.sha256(a1.read_bytes()).hexdigest()[:16]
    if fin:
        rec["final_sha256"] = hashlib.sha256(fin.read_bytes()).hexdigest()[:16]
    same = bool(a1 and fin and rec["attempt1_sha256"] == rec["final_sha256"])
    rec["final_differs_from_attempt1"] = bool(a1 and fin and not same)

    if a1:
        rec["attempt1_public_pass"] = run_suite(task_dir, "tests_public", a1, work)["passed"]
        rec["attempt1_hidden_pass"] = run_suite(task_dir, "tests_hidden", a1, work)["passed"]
    if fin:
        if same and dedupe:
            rec["final_public_pass"] = rec["attempt1_public_pass"]
            rec["final_hidden_pass"] = rec["attempt1_hidden_pass"]
            rec["final_graded_separately"] = False
        else:
            rec["final_public_pass"] = run_suite(task_dir, "tests_public", fin, work)["passed"]
            rec["final_hidden_pass"] = run_suite(task_dir, "tests_hidden", fin, work)["passed"]
            rec["final_graded_separately"] = True
    else:
        rec["final_graded_separately"] = False
    return rec


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------
FIELDS = [
    "run", "model_label", "model_id", "prompt", "prompt_variant", "task",
    "attempt1_present", "final_present",
    "attempt1_sha256", "final_sha256", "final_differs_from_attempt1",
    "final_graded_separately",
    "attempt1_public_pass", "attempt1_hidden_pass",
    "final_public_pass", "final_hidden_pass",
    "repair_eligible", "repair_attempted", "no_repair_reason",
    "repair_produced_code", "repair_public_pass_logged",
    "logged_attempt1_public_pass", "logged_attempt1_from_cache",
    "log_matches_regrade_public",
    "hidden_fail_to_pass", "hidden_pass_to_fail",
    "a1_finish_reason", "a1_truncated", "a1_prompt_tokens",
    "a1_completion_tokens", "a1_total_tokens", "a1_reasoning_tokens",
    "a1_cached_tokens", "a1_wall_s",
    "a2_finish_reason", "a2_truncated", "a2_prompt_tokens",
    "a2_completion_tokens", "a2_total_tokens", "a2_reasoning_tokens",
    "a2_cached_tokens", "a2_wall_s",
    "api_calls", "api_errors", "cache_hit", "no_program", "budget_skip",
    "reported_hidden_pass", "reported_matches_regrade",
]


def pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.1f}%" if d else "n/a"


def build_summary(rows: list[dict], configs: list[dict], n_tasks_expected: int) -> str:
    by_run: dict[str, list[dict]] = {}
    for r in rows:
        by_run.setdefault(r["run"], []).append(r)

    L: list[str] = []
    L.append("# Repair pipeline reported in parts (r2 run)")
    L.append("")
    L.append(
        "Produced by `scripts/r2_repair_audit.py`. Every first attempt and every "
        "final solution was graded from scratch against the public suite and the "
        "hidden suite, in an isolated directory holding the task source and "
        "exactly one suite. The repair decision fields come from `events.jsonl`, "
        "which the run wrote at the moment each decision was taken."
    )
    L.append("")
    L.append("## Column meanings")
    L.append("")
    L.append(
        "* Attempt 1 public pass: the first generated program passed the public "
        "tests. These tasks are not eligible for repair."
    )
    L.append(
        "* Repair eligible: the first program failed the public tests, which is "
        "the condition the pipeline uses to fire the repair."
    )
    L.append(
        "* Repairs attempted: an eligible task for which a second API call was "
        "issued. Skipped tasks are eligible tasks with no second call, and the "
        "reason is given in the next table."
    )
    L.append(
        "* Repairs passing public: repaired programs that passed the public "
        "tests afterwards."
    )
    L.append(
        "* Initial hidden pass: the first attempt graded on the hidden tests. "
        "Final hidden pass: the scored solution graded on the hidden tests."
    )
    L.append("")
    L.append("## Repair pipeline per configuration")
    L.append("")
    L.append(
        "| Configuration | Prompt | Tasks graded | Status | Attempt 1 available | "
        "Attempt 1 public pass | Repair eligible | Repairs attempted | Repairs skipped | "
        "Repairs passing public | Initial hidden pass | Final hidden pass | "
        "Hidden fail to pass | Hidden pass to fail |"
    )
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for cfg in configs:
        rs = by_run.get(cfg["run"])
        if not rs:
            continue
        n = len(rs)
        status = "complete" if n >= n_tasks_expected else f"incomplete ({n}/{n_tasks_expected})"
        n_a1 = sum(1 for r in rs if r["attempt1_present"])
        n_fin = sum(1 for r in rs if r["final_present"])
        a1_pub = sum(1 for r in rs if r["attempt1_public_pass"] is True)
        eligible = sum(1 for r in rs if r["repair_eligible"] is True)
        attempted = sum(1 for r in rs if r["repair_attempted"] is True)
        skipped = eligible - attempted
        rep_pub = sum(1 for r in rs if r["repair_public_pass_logged"] is True)
        a1_hid = sum(1 for r in rs if r["attempt1_hidden_pass"] is True)
        fin_hid = sum(1 for r in rs if r["final_hidden_pass"] is True)
        gain = sum(1 for r in rs if r["hidden_fail_to_pass"] is True)
        loss = sum(1 for r in rs if r["hidden_pass_to_fail"] is True)
        L.append(
            f"| {cfg['label']} | {cfg['prompt']} | {n} | {status} | {n_a1} | "
            f"{a1_pub} ({pct(a1_pub, n_a1)}) | {eligible} | {attempted} | {max(0, skipped)} | "
            f"{rep_pub} | {a1_hid} ({pct(a1_hid, n_a1)}) | {fin_hid} ({pct(fin_hid, n_fin)}) | "
            f"{gain} | {loss} |"
        )
    L.append("")
    L.append(
        "The two attempt 1 percentages are shares of the tasks that have a stored "
        "first attempt. The final hidden percentage is a share of the tasks that "
        "have a stored final solution. Both denominators equal 185 only when the "
        "row is marked complete."
    )
    L.append("")

    L.append("## Reasons a repair was not attempted")
    L.append("")
    L.append(
        "`passed` means the first attempt already passed the public tests. "
        "`no_repair_flag` means the repair step was disabled for that call. "
        "`over_budget` means the token budget was exhausted before the repair. "
        "`missing` means no repair decision was logged for the task."
    )
    L.append("")
    L.append(
        "| Configuration | Prompt | passed | no_repair_flag | over_budget | missing | "
        "Eligible but skipped |"
    )
    L.append("|---|---|---|---|---|---|---|")
    for cfg in configs:
        rs = by_run.get(cfg["run"])
        if not rs:
            continue
        counts = {k: 0 for k in NO_REPAIR_REASONS}
        counts["missing"] = 0
        for r in rs:
            reason = r["no_repair_reason"]
            if r["repair_attempted"] is True:
                continue
            if reason in counts:
                counts[reason] += 1
            else:
                counts["missing"] += 1
        eligible = sum(1 for r in rs if r["repair_eligible"] is True)
        attempted = sum(1 for r in rs if r["repair_attempted"] is True)
        L.append(
            f"| {cfg['label']} | {cfg['prompt']} | {counts['passed']} | "
            f"{counts['no_repair_flag']} | {counts['over_budget']} | "
            f"{counts['missing']} | {max(0, eligible - attempted)} |"
        )
    L.append("")

    L.append("## Data completeness and consistency")
    L.append("")
    L.append(
        "| Configuration | Prompt | Tasks graded | Missing attempt 1 | Missing final | "
        "No program | Budget skips | API errors | Log and regrade disagree | "
        "Runner results disagree |"
    )
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for cfg in configs:
        rs = by_run.get(cfg["run"])
        if not rs:
            continue
        L.append(
            f"| {cfg['label']} | {cfg['prompt']} | {len(rs)} | "
            f"{sum(1 for r in rs if not r['attempt1_present'])} | "
            f"{sum(1 for r in rs if not r['final_present'])} | "
            f"{sum(1 for r in rs if r['no_program'])} | "
            f"{sum(1 for r in rs if r['budget_skip'])} | "
            f"{sum(int(r['api_errors'] or 0) for r in rs)} | "
            f"{sum(1 for r in rs if r['log_matches_regrade_public'] is False)} | "
            f"{sum(1 for r in rs if r['reported_matches_regrade'] is False)} |"
        )
    L.append("")
    L.append(
        "The last column is empty of meaning until the runner has written "
        "`results.csv` for a configuration. Rows with no recorded value are not "
        "counted as disagreements."
    )
    L.append("")

    incomplete = [
        cfg["run"] for cfg in configs
        if len(by_run.get(cfg["run"], [])) < n_tasks_expected
    ]
    if incomplete:
        L.append("## Incomplete configurations")
        L.append("")
        L.append(
            "The following configurations were graded on fewer than "
            f"{n_tasks_expected} tasks, so their numbers are a progress check and "
            "not a final result: " + ", ".join(incomplete) + "."
        )
        L.append("")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--pattern", default="r2-*", help="run directory glob")
    ap.add_argument("--configs", default="", help="comma separated run names to keep")
    ap.add_argument("--tasks", default="", help="comma separated task ids to keep")
    ap.add_argument("--limit", type=int, default=0, help="first N tasks only")
    ap.add_argument("--out-dir", default=str(REPORTS))
    ap.add_argument("--expected-tasks", type=int, default=EXPECTED_TASKS)
    ap.add_argument(
        "--no-dedupe",
        action="store_true",
        help="grade the final solution even when it is byte identical to attempt 1",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    tasks = task_dirs()
    if args.tasks:
        keep = {t.strip() for t in args.tasks.split(",") if t.strip()}
        tasks = [t for t in tasks if t.name in keep]
    if args.limit:
        tasks = tasks[: args.limit]

    configs = discover_configs(args.pattern)
    if args.configs:
        keep = {c.strip() for c in args.configs.split(",") if c.strip()}
        configs = [c for c in configs if c["run"] in keep or c["run"].removeprefix("r2-") in keep]
    if not configs:
        print("no configurations matched", file=sys.stderr)
        sys.exit(1)

    # Only grade tasks that have at least one stored program, so a run still in
    # progress is reported on what it has rather than on 185 empty rows.
    jobs = []
    per_run_paths: dict[tuple[str, str], tuple[Path | None, Path | None]] = {}
    for cfg in configs:
        for t in tasks:
            a1, fin = solution_paths(cfg, t.name)
            if not a1 and not fin:
                continue
            per_run_paths[(cfg["run"], t.name)] = (a1, fin)
            jobs.append((cfg["run"], t, a1, fin, not args.no_dedupe))

    print(
        f"grading {len(jobs)} tasks across {len(configs)} configurations "
        f"({args.workers} workers)",
        flush=True,
    )

    graded: dict[tuple[str, str], dict] = {}
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, rec in enumerate(ex.map(grade_task, jobs), 1):
            graded[(rec["run"], rec["task"])] = rec
            if i % 100 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)}  {round(time.time() - t0)}s", flush=True)

    rows: list[dict] = []
    for cfg in configs:
        events = load_events(cfg["dir"])
        reported = reported_hidden(cfg["dir"])
        for t in tasks:
            g = graded.get((cfg["run"], t.name))
            if not g:
                continue
            ev = events.get(t.name, {})
            dec = ev.get("repair_decision") or {}
            res = ev.get("repair_result") or {}
            c1 = last_call(ev, 1)
            c2 = last_call(ev, 2)

            # Eligibility is the condition the pipeline itself evaluated, so the
            # logged value wins. The regrade is the fallback when no decision
            # was logged, and the two are compared in `log_matches_regrade_public`.
            logged_pub = dec.get("attempt1_public_pass")
            regrade_pub = g["attempt1_public_pass"]
            if logged_pub is not None:
                eligible = logged_pub is False
                log_match = "" if regrade_pub == "" else bool(logged_pub) == bool(regrade_pub)
            elif regrade_pub != "":
                eligible = regrade_pub is False
                log_match = ""
            else:
                eligible = None
                log_match = ""

            a1_hid = g["attempt1_hidden_pass"]
            fin_hid = g["final_hidden_pass"]
            both = a1_hid != "" and fin_hid != ""
            rep = reported.get(t.name)

            row = {
                "run": cfg["run"],
                "model_label": cfg["label"],
                "model_id": cfg["model_id"],
                "prompt": cfg["prompt"],
                "prompt_variant": cfg["prompt_variant"],
                "repair_eligible": eligible if eligible is not None else "",
                "repair_attempted": dec.get("repair_attempted", ""),
                "no_repair_reason": dec.get("no_repair_reason") or "",
                "repair_produced_code": res.get("repair_produced_code", ""),
                "repair_public_pass_logged": res.get("repair_public_pass", ""),
                "logged_attempt1_public_pass": "" if logged_pub is None else logged_pub,
                "logged_attempt1_from_cache": dec.get("attempt1_from_cache", ""),
                "log_matches_regrade_public": log_match,
                "hidden_fail_to_pass": (a1_hid is False and fin_hid is True) if both else "",
                "hidden_pass_to_fail": (a1_hid is True and fin_hid is False) if both else "",
                "api_calls": len(ev.get("api_calls", [])),
                "api_errors": len(ev.get("api_errors", [])),
                "cache_hit": ev.get("cache_hit", False),
                "no_program": ev.get("no_program", False),
                "budget_skip": ev.get("budget_skip", False),
                "reported_hidden_pass": "" if rep is None else rep,
                "reported_matches_regrade": (
                    "" if rep is None or fin_hid == "" else bool(rep) == bool(fin_hid)
                ),
            }
            row.update(g)
            row.update(attempt_columns(c1, "a1"))
            row.update(attempt_columns(c2, "a2"))
            rows.append(row)

    csv_path = out_dir / "r2_repair_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)

    md_path = out_dir / "r2_repair_summary.md"
    md_path.write_text(build_summary(rows, configs, args.expected_tasks), encoding="utf-8")

    print(f"\nwrote {csv_path}")
    print(f"wrote {md_path}")
    print(f"rows: {len(rows)}   elapsed: {round(time.time() - t0)}s")


if __name__ == "__main__":
    main()
