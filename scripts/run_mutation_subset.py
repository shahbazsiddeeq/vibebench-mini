#!/usr/bin/env python3
"""
Run mutmut on a stratified subset of tasks (3 per category) for each agent.
Updates the agent's results.csv with mutation scores for those tasks.

Usage:
  python scripts/run_mutation_subset.py [--agents agent1 agent2 ...]

Requires: mutmut  (pip install mutmut)
Estimated time: ~5–10 min per agent (30 tasks × ~10–20s each)
"""
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / ".agent_runs"
TASKS = ROOT / "tasks" / "python"
CATS_FILE = ROOT / "tasks" / "categories.json"

# 3 tasks per category, chosen to be representative and fast (small test suites)
MUTATION_SUBSET = [
    # ADS
    "task01",
    "task018",
    "task022",
    # SPT
    "task02",
    "task03",
    "task13",
    # FIO
    "task05",
    "task053",
    "task060",
    # CAT
    "task038",
    "task063",
    "task067",
    # DBS
    "task073",
    "task074",
    "task077",
    # WNT
    "task08",
    "task084",
    "task087",
    # CCA
    "task091",
    "task093",
    "task105",
    # DPS
    "task06",
    "task094",
    "task096",
    # ODP
    "task101",
    "task102",
    "task104",
    # TCQ
    "task107",
    "task108",
    "task15",
]

DEFAULT_AGENTS = [
    "openai-default",
    "gpt-4o",
    "claude-haiku",
    "claude-sonnet",
    "openai-secure",
    "gpt-4o-secure",
    "claude-haiku-secure",
    "claude-sonnet-secure",
]


def run_mutmut(workspace: Path) -> tuple[int | None, int | None, float | None]:
    """Run mutmut 2.x on workspace/src against workspace/tests. Return (killed, total, score)."""
    import xml.etree.ElementTree as ET

    if shutil.which("mutmut") is None:
        print(
            "  mutmut not found — install with: pip install 'mutmut<3'", file=sys.stderr
        )
        return None, None, None

    # Clean up any stale artifacts from previous runs
    for artifact in [".mutmut-cache", "mutants"]:
        p = workspace / artifact
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.exists():
            p.unlink(missing_ok=True)
    for pyc in workspace.rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "mutmut",
            "run",
            "--paths-to-mutate",
            "src",
            "--tests-dir",
            "tests",
            "--no-progress",
        ],
        cwd=workspace,
        capture_output=True,
        timeout=120,
    )

    # Use junitxml for reliable killed/survived counts
    r = subprocess.run(
        [sys.executable, "-m", "mutmut", "junitxml"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if r.returncode != 0 or not r.stdout.strip():
        return None, None, None

    try:
        root = ET.fromstring(r.stdout)
        suite = root.find("testsuite") or root
        total = int(suite.get("tests", 0))
        survived = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
    except Exception:
        return None, None, None

    if total == 0:
        return 0, 0, None
    killed = total - survived
    score = killed / total
    return killed, total, score


def build_workspace(agent_run: Path, task_id: str) -> Path | None:
    """Copy reference task + agent solution into a temp dir for mutmut."""
    ref_task = TASKS / task_id
    if not ref_task.exists():
        return None

    agent_task = agent_run / "tasks" / "python" / task_id
    solution = agent_task / "src" / "solution.py"
    if not solution.exists():
        return None

    tmp = Path(tempfile.mkdtemp(prefix=f"mutmut_{task_id}_"))
    shutil.copytree(ref_task, tmp, dirs_exist_ok=True)
    (tmp / "src" / "solution.py").write_text(
        solution.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return tmp


def load_results(agent: str) -> list[dict]:
    p = RUNS / agent / "results.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_results(agent: str, rows: list[dict]) -> None:
    p = RUNS / agent / "results.csv"
    if not rows:
        return
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--agents",
        nargs="+",
        default=None,
        help="Agent names to run mutation on (default: all available)",
    )
    ap.add_argument(
        "--tasks",
        nargs="+",
        default=None,
        help="Override task subset (default: built-in 30-task stratified subset)",
    )
    args = ap.parse_args()

    if shutil.which("mutmut") is None:
        print("ERROR: mutmut not installed. Run: pip install mutmut")
        sys.exit(1)

    subset = args.tasks or MUTATION_SUBSET
    agents_to_run = args.agents or [
        a for a in DEFAULT_AGENTS if (RUNS / a / "results.csv").exists()
    ]

    if not agents_to_run:
        print("No agent results found. Run experiments first.")
        sys.exit(1)

    print(f"Running mutation on {len(subset)} tasks × {len(agents_to_run)} agents")
    print(f"Agents: {agents_to_run}")
    print(f"Tasks:  {subset}\n")

    for agent in agents_to_run:
        rows = load_results(agent)
        if not rows:
            print(f"[{agent}] no results.csv — skipping")
            continue

        id_to_row = {r["id"]: r for r in rows if r.get("id") != "__aggregate__"}
        changed = 0

        for task_id in subset:
            if task_id not in id_to_row:
                print(f"  [{agent}] {task_id} not in results — skip")
                continue

            workspace = build_workspace(RUNS / agent, task_id)
            if workspace is None:
                print(f"  [{agent}] {task_id} no solution found — skip")
                continue

            print(f"  [{agent}] {task_id} ... ", end="", flush=True)
            try:
                killed, total, score = run_mutmut(workspace)
            except subprocess.TimeoutExpired:
                killed, total, score = None, None, None
                print("TIMEOUT")
            else:
                if score is not None:
                    print(f"{killed}/{total} killed  score={score:.3f}")
                else:
                    print("no mutants")
            finally:
                shutil.rmtree(workspace, ignore_errors=True)

            row = id_to_row[task_id]
            row["mutation_killed"] = killed if killed is not None else ""
            row["mutation_total"] = total if total is not None else ""
            row["mutation_score"] = f"{score:.6f}" if score is not None else ""
            changed += 1

        if changed:
            # rebuild rows list preserving __aggregate__ row at end
            agg_rows = [r for r in rows if r.get("id") == "__aggregate__"]
            data_rows = [r for r in rows if r.get("id") != "__aggregate__"]
            save_results(agent, data_rows + agg_rows)
            print(f"  [{agent}] saved {changed} mutation results to results.csv\n")


if __name__ == "__main__":
    main()
