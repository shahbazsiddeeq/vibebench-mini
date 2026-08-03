#!/usr/bin/env python3.12
"""Mutation-based validation of every CodeAssay test suite.

The paper reported mutation evidence from a
sample of 15 tasks. This script runs mutation analysis over all 185 reference
suites so the adequacy claim covers the whole benchmark rather than a sample.

Why the earlier attempt returned zero mutants
---------------------------------------------
`scripts/validate_test_suites.py` was diagnosed as a PYTHONPATH problem. That was
wrong. The actual failure is a pytest module-basename collision: a task directory
holds `tests/test_solution.py`, `tests_public/test_solution.py` and
`tests_hidden/test_solution.py`, three modules with the same basename and no
`__init__.py`, plus committed `__pycache__` directories. pytest resolves the
module name from the basename, finds a stale `.pyc` from a sibling directory and
aborts collection with "import file mismatch", so mutmut's baseline run fails and
no mutants are ever generated.

The fix here is to stage each task into a scratch directory that contains the
source and exactly one test suite, with all `__pycache__` removed, and to give
mutmut an explicit runner (`python3.12 -m pytest`, since bare `python` does not
exist in this environment). The benchmark tree itself is never modified.

Mutation score = (killed + timeout) / (killed + survived + timeout + suspicious).
A mutant that makes the suite hang is detected by the suite, so timeouts count as
detected; the raw per-status counts are released so any other convention can be
recomputed. A suite is called discriminative when no mutant survives.

Run:
  python3.12 scripts/mutation_validate.py --tests tests_hidden --workers 8
  python3.12 scripts/mutation_validate.py --tests tests --workers 8   # full suite
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks" / "python"
REPORTS = ROOT / "reports"
SCRATCH = ROOT / ".mutation_scratch"
PY = "python3.12"

BUCKETS = ("Killed", "Survived", "Timeout", "Suspicious")


def stage(task_dir: Path, tests_dir: str, dest_root: Path) -> Path:
    """Copy src plus exactly one suite into a clean scratch task directory."""
    dest = dest_root / task_dir.name
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "src").mkdir(parents=True)
    for f in (task_dir / "src").glob("*.py"):
        shutil.copy(f, dest / "src" / f.name)
    (dest / "tests").mkdir()
    for f in (task_dir / tests_dir).glob("*.py"):
        shutil.copy(f, dest / "tests" / f.name)
    # Any requirements the task declares are irrelevant to mutation of the
    # reference, but a conftest keeps the task root importable without relying
    # on the caller's PYTHONPATH.
    (dest / "conftest.py").write_text(
        "import os, sys\nsys.path.insert(0, os.path.dirname(__file__))\n",
        encoding="utf-8",
    )
    return dest


def read_cache(work: Path) -> dict[str, int]:
    """Read mutant outcomes straight from mutmut's SQLite cache.

    `mutmut results` prints only mutants that were NOT killed, so an empty
    listing is indistinguishable from "no mutants were generated". Reading the
    cache gives the exact per-status counts either way.
    """
    db = work / ".mutmut-cache"
    if not db.exists():
        return {}
    con = sqlite3.connect(str(db))
    try:
        rows = con.execute("select status, count(*) from Mutant group by status")
        return {status: n for status, n in rows}
    except sqlite3.Error:
        return {}
    finally:
        con.close()


def run_task(task_dir: Path, tests_dir: str, timeout: int) -> dict:
    name = task_dir.name
    t0 = time.time()
    rec: dict = {"task": name, "tests_dir": tests_dir}
    try:
        work = stage(task_dir, tests_dir, SCRATCH)
    except Exception as exc:  # staging is local IO; surface but do not abort
        rec.update(status="stage_error", error=str(exc)[:200])
        return rec

    base = subprocess.run(
        [PY, "-m", "pytest", "-x", "-q", "tests"],
        cwd=work, capture_output=True, text=True, timeout=300,
    )
    if base.returncode != 0:
        rec.update(
            status="baseline_failed",
            error=(base.stdout or base.stderr)[-400:],
            seconds=round(time.time() - t0, 1),
        )
        return rec

    try:
        subprocess.run(
            [PY, "-m", "mutmut", "run",
             "--paths-to-mutate", "src",
             "--tests-dir", "tests",
             "--no-progress",
             "--runner", f"{PY} -m pytest -x -q"],
            cwd=work, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        rec.update(status="timeout", seconds=round(time.time() - t0, 1))
        return rec

    vals = read_cache(work)
    killed = vals.get("ok_killed", 0)
    survived = vals.get("bad_survived", 0)
    timeout_m = vals.get("bad_timeout", 0)
    suspicious = vals.get("ok_suspicious", 0)
    total = killed + survived + timeout_m + suspicious
    # A mutant that makes the suite hang is detected by the suite, so timeouts
    # count as killed. Raw buckets are kept so any other convention can be
    # recomputed from the released data.
    detected = killed + timeout_m
    rec.update(
        status="ok" if total else "no_mutants",
        killed=killed,
        survived=survived,
        timeout_mutants=timeout_m,
        suspicious=suspicious,
        total=total,
        score=round(detected / total, 4) if total else None,
        discriminative=(total > 0 and survived == 0),
        seconds=round(time.time() - t0, 1),
    )
    shutil.rmtree(work, ignore_errors=True)
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", default="tests_hidden",
                    choices=["tests_hidden", "tests_public", "tests"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    REPORTS.mkdir(exist_ok=True)
    SCRATCH.mkdir(exist_ok=True)

    tasks = sorted(TASKS.glob("task*"))
    tasks = [t for t in tasks if (t / "src" / "solution.py").exists()
             and (t / args.tests).exists()]
    if args.limit:
        tasks = tasks[: args.limit]
    print(f"mutation validation on {len(tasks)} tasks, suite={args.tests}, "
          f"workers={args.workers}", flush=True)

    out_path = REPORTS / f"mutation_validation_{args.tests}.json"
    records: list[dict] = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_task, t, args.tests, args.timeout): t for t in tasks}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            try:
                rec = fut.result()
            except Exception as exc:
                rec = {"task": futs[fut].name, "status": "error",
                       "error": str(exc)[:200]}
            records.append(rec)
            if i % 10 == 0 or i == len(tasks):
                ok = [r for r in records if r.get("status") == "ok"]
                print(f"  {i}/{len(tasks)} done, {len(ok)} scored, "
                      f"{round(time.time()-t0)}s elapsed", flush=True)
                out_path.write_text(json.dumps(records, indent=1), encoding="utf-8")

    records.sort(key=lambda r: r["task"])
    out_path.write_text(json.dumps(records, indent=1), encoding="utf-8")

    ok = [r for r in records if r.get("status") == "ok"]
    bad = [r for r in records if r.get("status") != "ok"]
    disc = [r for r in ok if r.get("discriminative")]
    weak = [r for r in ok if not r.get("discriminative")]
    tot_m = sum(r["total"] for r in ok)
    tot_k = sum(r["killed"] + r["timeout_mutants"] for r in ok)

    L = [f"# Mutation validation of the CodeAssay test suites (`{args.tests}`)", ""]
    L.append(
        "Produced by `scripts/mutation_validate.py`. Mutants are generated from "
        "each task's reference solution with mutmut and executed against that "
        "task's suite. A suite counts as discriminative when no mutant survives."
    )
    L.append("")
    L.append(f"- Tasks attempted: {len(records)}")
    L.append(f"- Tasks scored: {len(ok)}")
    if bad:
        L.append(f"- Tasks not scored: {len(bad)} ({', '.join(sorted(set(r.get('status','?') for r in bad)))})")
    L.append(f"- Mutants generated: {tot_m}")
    L.append(f"- Mutants killed: {tot_k}")
    if tot_m:
        L.append(f"- Overall mutation score: {tot_k/tot_m:.3f}")
    L.append(f"- Suites killing every mutant: {len(disc)} of {len(ok)}")
    L.append("")
    if weak:
        L.append("## Suites with surviving mutants")
        L.append("")
        L.append("| Task | Killed | Survived | Total | Score |")
        L.append("|---|---|---|---|---|")
        for r in sorted(weak, key=lambda r: r["score"] or 0):
            L.append(f"| {r['task']} | {r['killed']} | {r['survived']} | "
                     f"{r['total']} | {r['score']:.3f} |")
        L.append("")
    if bad:
        L.append("## Tasks not scored")
        L.append("")
        L.append("| Task | Status | Detail |")
        L.append("|---|---|---|")
        for r in sorted(bad, key=lambda r: r["task"]):
            det = " ".join((r.get("error") or "").split())[:120]
            L.append(f"| {r['task']} | {r.get('status')} | {det} |")
        L.append("")

    md = REPORTS / f"mutation_validation_{args.tests}.md"
    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\nwrote {md}")
    print(f"wrote {out_path}")
    print(f"scored {len(ok)}/{len(records)}; overall score "
          f"{tot_k/tot_m:.3f}" if tot_m else "no mutants")


if __name__ == "__main__":
    sys.exit(main())
