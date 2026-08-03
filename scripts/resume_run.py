#!/usr/bin/env python3
"""
Resume the 10-agent x 138-task run WITHOUT redoing finished agents.

An agent is considered DONE if .agent_runs/<name>/results.csv exists and has
exactly 138 data rows (the finalized task count). Stale 120-row files from the
prior run and half-finished agents are treated as NOT done and will be re-run.

Usage:
    set -a; . ./.env; set +a          # load API keys
    python scripts/resume_run.py          # report status + write resume config
    python scripts/resume_run.py --run    # also run the pending agents

The full config (configs/agents.profes10.yaml) re-runs ALL agents; always use
THIS script (or the generated configs/agents.profes_resume.yaml) to resume.
"""
from __future__ import annotations
import argparse, csv, re, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "configs" / "agents.profes10.yaml"
RESUME = ROOT / "configs" / "agents.profes_resume.yaml"
RUNS = ROOT / ".agent_runs"
EXPECTED_ROWS = 185  # number of task rows (the trailing __aggregate__ row is ignored)
TASK_RE = re.compile(r"^task[0-9]+$")


def data_rows(csv_path: Path) -> int:
    """Count scored TASK rows (ignores header and the __aggregate__ summary row)."""
    if not csv_path.exists():
        return -1
    with csv_path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        return sum(1 for row in reader if row and TASK_RE.match(row[0]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="run the pending agents after reporting")
    args = ap.parse_args()

    cfg = yaml.safe_load(FULL.read_text())
    agents = cfg["agents"]
    done, pending = [], []
    for a in agents:
        rows = data_rows(RUNS / a["name"] / "results.csv")
        (done if rows == EXPECTED_ROWS else pending).append((a, rows))

    print("=== agent status (results.csv data rows; need %d) ===" % EXPECTED_ROWS)
    for a, rows in done:
        print(f"  DONE    {a['name']:22} ({rows} rows)")
    for a, rows in pending:
        state = "missing" if rows < 0 else (f"{rows} rows" + (" [stale/old]" if rows == 120 else " [partial]"))
        print(f"  PENDING {a['name']:22} ({state})")

    if not pending:
        print("\nAll 10 agents complete. Nothing to resume. Proceed to mutation/stats.")
        return

    RESUME.write_text(yaml.safe_dump({"agents": [a for a, _ in pending]}, sort_keys=False))
    print(f"\nWrote resume config ({len(pending)} pending agents): {RESUME}")

    if args.run:
        print("Running pending agents...\n")
        rc = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_agents.py"),
                             "--config", str(RESUME)]).returncode
        sys.exit(rc)
    else:
        print("Re-run with --run to execute, e.g.:")
        print("  set -a; . ./.env; set +a && python scripts/resume_run.py --run")


if __name__ == "__main__":
    main()
