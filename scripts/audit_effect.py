#!/usr/bin/env python3
"""Measure what the audit-and-fix actually changed.

The audit repaired references and strengthened tests before any model was scored.
The paper reports the process (assertions grown, tasks dropped) but not its
effect. This script measures the effect directly and without any API calls: it
grades every stored generated program against BOTH the pre-audit test suite and
the post-audit one, and reports how many programs the pre-audit suites would have
accepted that the post-audit suites reject.

The pre-audit tree is checkpoints/tasks_BACKUP_pre_restasks_2026-07-25/python.
Only tasks present in both trees are used (the other 50 released tasks were
authored after that snapshot), and both sides are graded on the FULL suite so the
comparison holds the notion of "the task's tests" constant. Grading pins
PYTHONHASHSEED for the same reason the main harness does.
"""

import argparse
import ast
import collections
import concurrent.futures as cf
import csv
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRE = ROOT / "checkpoints" / "tasks_BACKUP_pre_restasks_2026-07-25" / "python"
CUR = ROOT / "tasks" / "python"
PY = sys.executable

CONFIGS = {
    "gpt4omini": "GPT-4o-mini", "gpt4o": "GPT-4o", "gpt56sol": "GPT-5.6-sol",
    "haiku45": "Claude Haiku 4.5", "sonnet45": "Claude Sonnet 4.5",
    "sonnet5": "Claude Sonnet 5", "gemini25": "Gemini 2.5 Flash",
}


def shared_tasks():
    cur = {p.name for p in CUR.glob("task*") if p.is_dir()}
    out = []
    for t in sorted(cur):
        if (PRE / t / "tests" / "test_solution.py").exists() and (CUR / t / "tests" / "test_solution.py").exists():
            out.append(t)
    return out


def run_suite(task_root: Path, solution: Path) -> bool:
    """Substitute the generated program into a copy of the task and run its suite."""
    tmp = tempfile.mkdtemp(prefix="auditeff_")
    try:
        os.makedirs(f"{tmp}/src", exist_ok=True)
        os.makedirs(f"{tmp}/tests", exist_ok=True)
        for f in (task_root / "src").glob("*.py"):
            shutil.copy(f, f"{tmp}/src/")
        shutil.copy(solution, f"{tmp}/src/solution.py")
        for f in (task_root / "tests").glob("*.py"):
            shutil.copy(f, f"{tmp}/tests/")
        Path(tmp, "conftest.py").write_text(
            "import os, sys\nsys.path.insert(0, os.path.dirname(__file__))\n")
        env = {**os.environ, "PYTHONHASHSEED": "0"}
        p = subprocess.run([PY, "-m", "pytest", "-q", "--disable-warnings", "tests"],
                           cwd=tmp, capture_output=True, text=True, timeout=180, env=env)
        return p.returncode == 0
    except Exception:
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def assertions(path: Path) -> int:
    try:
        return sum(1 for x in ast.walk(ast.parse(path.read_text(errors="ignore")))
                   if isinstance(x, ast.Assert))
    except Exception:
        return 0


def grade(job):
    slug, prompt, task = job
    hits = glob.glob(str(ROOT / f".agent_runs/r2-{slug}-{prompt}/cache/{task}__*.py"))
    if not hits:
        return None
    sol = Path(hits[0])
    return {
        "config": f"{slug}-{prompt}", "model": CONFIGS[slug], "prompt": prompt, "task": task,
        "pre_audit_pass": run_suite(PRE / task, sol),
        "post_audit_pass": run_suite(CUR / task, sol),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="first N tasks only (smoke test)")
    args = ap.parse_args()

    tasks = shared_tasks()
    if args.limit:
        tasks = tasks[: args.limit]
    jobs = [(s, p, t) for s in CONFIGS for p in ("std", "sec") for t in tasks]
    print(f"tasks in both trees: {len(tasks)}   gradings: {len(jobs) * 2}", flush=True)

    rows = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, r in enumerate(ex.map(grade, jobs), 1):
            if r:
                rows.append(r)
            if i % 200 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)

    out = ROOT / "reports" / "audit_effect.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    per = collections.defaultdict(lambda: [0, 0, 0])  # pre, post, accepted-then-rejected
    for r in rows:
        k = (r["model"], r["prompt"])
        per[k][0] += r["pre_audit_pass"]
        per[k][1] += r["post_audit_pass"]
        per[k][2] += (r["pre_audit_pass"] and not r["post_audit_pass"])

    n = len(tasks)
    lines = [
        "# What the audit changed",
        "",
        f"Every stored program for the {n} tasks present in both the pre-audit snapshot "
        f"and the released benchmark, graded against each task's full suite before and "
        f"after the audit-and-fix. No model output was regenerated.",
        "",
        f"Pre-audit assertions over these tasks: {sum(assertions(PRE / t / 'tests' / 'test_solution.py') for t in tasks)}; "
        f"after the audit: {sum(assertions(CUR / t / 'tests' / 'test_solution.py') for t in tasks)}.",
        "",
        "| Configuration | Prompt | Pre-audit correct | Post-audit correct | Change (pp) | Accepted then rejected |",
        "|---|---|---|---|---|---|",
    ]
    tot = [0, 0, 0]
    for m in CONFIGS.values():
        for p in ("std", "sec"):
            pre, post, flip = per[(m, p)]
            tot[0] += pre; tot[1] += post; tot[2] += flip
            lines.append(f"| {m} | {p} | {pre} ({100*pre/n:.1f}%) | {post} ({100*post/n:.1f}%) "
                         f"| {100*(post-pre)/n:+.1f} | {flip} |")
    lines += ["",
              f"Across all fourteen configurations, {tot[2]} of {14*n} stored programs pass the "
              f"pre-audit suite and fail the audited one. Aggregate correctness falls from "
              f"{100*tot[0]/(14*n):.1f}% to {100*tot[1]/(14*n):.1f}%."]
    (ROOT / "reports" / "audit_effect.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-3:]))
    print(f"wrote {out} and reports/audit_effect.md")


if __name__ == "__main__":
    main()
