#!/usr/bin/env python3
"""
FULL mutation testing with per-task checkpointing (crash/sleep safe).

For each --agent, over ALL tasks:
  - skip tasks already attempted (sidecar reports/mutation_done_<agent>.txt) -> resumable, never redone
  - only run mutmut when the agent's solution passes its suite (correctness == 1.0; mutmut needs a green baseline)
  - run mutmut (junitxml parsing) with a per-task timeout
  - SAVE results.csv + sidecar AFTER EVERY TASK  <-- the checkpoint the old script lacked

Usage: python scripts/run_mutation_full.py --agents claude-sonnet [--limit N]
Env: MUTMUT_TIMEOUT_S (default 600), PYTEST via venv python.
"""
from __future__ import annotations
import argparse, csv, os, shutil, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "'.agent_runs'".strip("'")
RUNS = ROOT / ".agent_runs"
TASKS = ROOT / "tasks" / "python"
REPORTS = ROOT / "reports"; REPORTS.mkdir(exist_ok=True)
ALL_TASKS = sorted((p.name for p in TASKS.iterdir() if p.is_dir() and p.name.startswith("task")),
                   key=lambda t: (len(t), t))
TIMEOUT = int(os.getenv("MUTMUT_TIMEOUT_S", "600"))


def run_mutmut(ws: Path):
    """Return ('score', killed, total, score_float) or a status string: 'timeout'|'error'|'nomut'."""
    for art in (".mutmut-cache", "mutants"):
        p = ws / art
        if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
        elif p.exists(): p.unlink(missing_ok=True)
    for pyc in ws.rglob("__pycache__"): shutil.rmtree(pyc, ignore_errors=True)
    env = dict(os.environ, PYTHONPATH=str(ws))
    try:
        subprocess.run([sys.executable, "-m", "mutmut", "run", "--paths-to-mutate", "src",
                        "--tests-dir", "tests", "--no-progress"],
                       cwd=ws, capture_output=True, timeout=TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return "timeout"
    try:
        r = subprocess.run([sys.executable, "-m", "mutmut", "junitxml"],
                           cwd=ws, capture_output=True, text=True, timeout=60, env=env)
    except subprocess.TimeoutExpired:
        return "timeout"
    if r.returncode != 0 or not r.stdout.strip():
        return "error"
    try:
        root = ET.fromstring(r.stdout)
        suite = root.find("testsuite")
        suite = suite if suite is not None else root
        total = int(suite.get("tests", 0))
        survived = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
    except Exception:
        return "error"
    if total == 0:
        return "nomut"
    killed = total - survived
    return ("score", killed, total, killed / total)


def build_ws(agent: str, task: str):
    ref = TASKS / task
    sol = RUNS / agent / "tasks" / "python" / task / "src" / "solution.py"
    if not ref.exists() or not sol.exists():
        return None
    tmp = Path(tempfile.mkdtemp(prefix=f"mut_{task}_"))
    shutil.copytree(ref, tmp, dirs_exist_ok=True)
    (tmp / "src" / "solution.py").write_text(sol.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp


def process(agent: str, limit: int | None):
    resfile = RUNS / agent / "results.csv"
    if not resfile.exists():
        print(f"[{agent}] no results.csv"); return
    done_file = REPORTS / f"mutation_done_{agent}.txt"
    done = set(done_file.read_text().split()) if done_file.exists() else set()
    with resfile.open() as f:
        rows = list(csv.DictReader(f))
    by = {r["id"]: r for r in rows if r["id"] != "__aggregate__"}
    fields = list(rows[0].keys())

    def save():
        with resfile.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        done_file.write_text("\n".join(sorted(done)))

    n = 0
    for task in ALL_TASKS:
        if task in done:
            continue
        row = by.get(task)
        if row is None:
            done.add(task); continue
        try:
            corr = float(row.get("correctness", 0) or 0)
        except ValueError:
            corr = 0.0
        if corr < 1.0:                       # baseline not green -> mutation N/A
            row["mutation_killed"] = ""; row["mutation_total"] = ""; row["mutation_score"] = ""
            done.add(task); save(); continue
        ws = build_ws(agent, task)
        if ws is None:
            done.add(task); save(); continue
        try:
            res = run_mutmut(ws)
        finally:
            shutil.rmtree(ws, ignore_errors=True)
        if isinstance(res, tuple):
            _, k, t, s = res
            row["mutation_killed"] = k; row["mutation_total"] = t; row["mutation_score"] = f"{s:.6f}"
            print(f"[{agent}] {task}: {k}/{t} score={s:.3f}", flush=True)
        else:                                 # timeout / error / nomut -> leave blank (excluded from stats)
            row["mutation_killed"] = ""; row["mutation_total"] = ""; row["mutation_score"] = ""
            print(f"[{agent}] {task}: {res}", flush=True)
        done.add(task); save()                # <-- CHECKPOINT after every task
        n += 1
        if limit and n >= limit:
            print(f"[{agent}] hit --limit {limit}, stopping"); break
    remaining = [t for t in ALL_TASKS if t not in done and t in by]
    print(f"[{agent}] processed {n} this run; {len(remaining)} tasks remain")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents", nargs="+", required=True)
    ap.add_argument("--limit", type=int, default=None, help="stop after N mutmut runs (for validation)")
    a = ap.parse_args()
    for ag in a.agents:
        process(ag, a.limit)
