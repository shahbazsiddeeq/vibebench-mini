#!/usr/bin/env python3
"""Benchmark validation via mutation testing.

Runs mutmut on each task's REFERENCE solution (src/solution.py) using the task's
test suite as the killing oracle, and reports the mutation score = killed/total.
A high score is evidence the benchmark tests actually catch bugs. This is a
one-time BENCHMARK-validation measurement, NOT a per-model code-quality axis.

By default it validates the HIDDEN suite (the grading oracle). Use --tests tests
to validate the full authored suite instead.

Usage:
  python scripts/validate_test_suites.py [--tests tests_hidden|tests|tests_public]
                                         [--limit N] [--python PY] [--out FILE]
Requires mutmut installed in the chosen interpreter.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys


def run(cmd, cwd, timeout):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def mutation_score(task_dir, tests_dir, py, timeout):
    cache = os.path.join(task_dir, ".mutmut-cache")
    if os.path.exists(cache):
        try:
            os.unlink(cache)
        except OSError:
            pass
    env = dict(os.environ, PYTHONPATH=".")
    subprocess.run(
        [py, "-m", "mutmut", "run", "--paths-to-mutate", "src",
         "--tests-dir", tests_dir, "--no-progress"],
        cwd=task_dir, capture_output=True, text=True, timeout=timeout, env=env,
    )
    code, out, _ = run([py, "-m", "mutmut", "results"], task_dir, 120)
    if code != 0:
        return None
    vals = {}
    for key in ("Survived", "Killed", "Timeout", "Suspicious"):
        m = re.search(rf"{key}\s*\((\d+)\)", out)
        vals[key] = int(m.group(1)) if m else 0
    total = sum(vals.values())
    if total == 0:
        return {"killed": 0, "total": 0, "score": None}
    return {"killed": vals["Killed"], "total": total,
            "score": round(vals["Killed"] / total, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", default="tests_hidden")
    ap.add_argument("--limit", type=int, default=0, help="0 = all tasks")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--out", default="tasks/python/test_suite_validation.json")
    ap.add_argument("--timeout", type=float, default=900)
    args = ap.parse_args()

    # sanity: mutmut present in the chosen interpreter?
    chk = subprocess.run([args.python, "-c", "import mutmut"], capture_output=True)
    if chk.returncode != 0:
        sys.exit(f"mutmut not importable by {args.python}; pip install mutmut in that env")

    tasks = sorted(glob.glob("tasks/python/task*/"))
    tasks = [t for t in tasks if os.path.isdir(os.path.join(t, args.tests))]
    if args.limit:
        tasks = tasks[:args.limit]

    report = {}
    scores = []
    for i, t in enumerate(tasks, 1):
        name = os.path.basename(t.rstrip("/"))
        try:
            r = mutation_score(t, args.tests, args.python, args.timeout)
        except Exception as e:  # noqa
            r = {"error": repr(e)[:160]}
        report[name] = r
        if r and r.get("score") is not None:
            scores.append(r["score"])
        print(f"[{i}/{len(tasks)}] {name}: {r}")

    summary = {
        "tests_dir": args.tests,
        "n_tasks": len(tasks),
        "n_scored": len(scores),
        "mean_mutation_score": round(sum(scores) / len(scores), 3) if scores else None,
        "min": min(scores) if scores else None,
        "max": max(scores) if scores else None,
    }
    json.dump({"summary": summary, "per_task": report},
              open(args.out, "w"), indent=2)
    print("\nSUMMARY:", summary)
    print("report:", args.out)


if __name__ == "__main__":
    main()
