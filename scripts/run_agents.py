#!/usr/bin/env python3
"""
Runs each agent defined in configs/agents.baseline.yaml over all tasks,
writes per-agent results under .agent_runs/<agent>/, and generates a
side-by-side comparison markdown at reports/agents_compare.md.
"""
from __future__ import annotations

import argparse
import csv
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs" / "agents.baseline.yaml"
RUNNER = ROOT / "runner" / "vibebench_runner.py"
TASKS_SRC = ROOT / "tasks" / "python"
RUNS = ROOT / ".agent_runs"
REPORTS = ROOT / "reports"


def runcmd(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    p = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True
    )
    return p.returncode, p.stdout, p.stderr


def discover_tasks() -> list[Path]:
    return sorted(
        [p for p in TASKS_SRC.iterdir() if p.is_dir() and (p / "tests").exists()]
    )


def find_test_file(task_dir: Path) -> Path:
    tests = sorted((task_dir / "tests").glob("test_*.py"))
    if not tests:
        raise FileNotFoundError(f"No tests found in {task_dir}")
    return tests[0]


def prepare_workspace(agent_name: str) -> Path:
    ws = RUNS / agent_name / "tasks" / "python"
    if ws.exists():
        shutil.rmtree(ws)
    shutil.copytree(TASKS_SRC, ws)
    return ws


def blank_solution(task_ws_task: Path, test_file: Path):
    sol = task_ws_task / "src" / "solution.py"
    sol.parent.mkdir(parents=True, exist_ok=True)
    # Provide a minimal importable stub (even if func name unknown)
    txt = test_file.read_text(encoding="utf-8")
    m = re.search(r"from\s+src\.solution\s+import\s+([A-Za-z_][A-Za-z0-9_]*)", txt)
    if m:
        func = m.group(1)
        code = f"def {func}(*args, **kwargs):\n    return None\n"
    else:
        code = "def solve(*args, **kwargs):\n    return None\n"
    sol.write_text(code, encoding="utf-8")


# def run_agent_on_task(cmd_tmpl: str, ws_task: Path, orig_task: Path):
#     test_file = find_test_file(orig_task)
#     # ensure a blank starting point so agent must write code:
#     blank_solution(ws_task, test_file)
#     cmd = cmd_tmpl.format(
#         task_dir=str(ws_task),
#         test_file=str(test_file),
#         orig_task_dir=str(orig_task),
#         ref=str(orig_task),
#     )
#     code, out, err = runcmd(cmd.split())
#     if code != 0:
#         print(
#             f"[warn] agent cmd failed for {ws_task.name}: {err.strip()}",
#             file=sys.stderr,
#         )

# def run_agent_on_task(cmd_tmpl: str, ws_task: Path, orig_task: Path, run_root: Path):
#     test_file = find_test_file(orig_task)
#     blank_solution(ws_task, test_file)
#     cmd = cmd_tmpl.format(
#         task_dir=str(ws_task),
#         test_file=str(test_file),
#         orig_task_dir=str(orig_task),
#         ref=str(orig_task),
#         run_root=str(run_root),
#     )
#     code, out, err = runcmd(cmd.split())
#     if code != 0:
#         print(f"[warn] agent cmd failed for {ws_task.name}: {err.strip()}", file=sys.stderr)


def run_agent_on_task(cmd_tmpl: str, ws_task: Path, orig_task: Path, run_root: Path):
    test_file = find_test_file(orig_task)
    blank_solution(ws_task, test_file)

    # Safely substitute placeholders and keep paths as single args even with spaces
    fmt = {
        "task_dir": shlex.quote(str(ws_task)),
        "test_file": shlex.quote(str(test_file)),
        "orig_task_dir": shlex.quote(str(orig_task)),
        "ref": shlex.quote(str(orig_task)),
        "run_root": shlex.quote(str(run_root)),
    }
    cmd_str = cmd_tmpl.format(**fmt)
    args = shlex.split(cmd_str)  # respects quotes

    # Ensure we run inside your venv’s Python, not system python
    if args and args[0] in ("python", "python3"):
        args[0] = sys.executable  # already imported above

    code, out, err = runcmd(args)
    if code != 0:
        print(
            f"[warn] agent cmd failed for {ws_task.name}: {err.strip()}",
            file=sys.stderr,
        )


def score_workspace(agent_name: str, ws_root: Path):
    out_json = RUNS / agent_name / "results.json"
    out_csv = RUNS / agent_name / "results.csv"
    code, out, err = runcmd(
        [
            sys.executable,
            str(RUNNER),
            "--tasks",
            str(ws_root / "tasks" / "python"),
            "--out",
            str(out_json),
            "--csv",
            str(out_csv),
        ]
    )
    if code != 0:
        print(err, file=sys.stderr)
        raise SystemExit(f"runner failed for {agent_name}")


def load_csv(path: Path) -> dict[str, dict[str, float]]:
    rows = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("id") == "__aggregate__":
                continue
            rows[r["id"]] = r
    return rows


def compare_agents(agents: list[str]):
    REPORTS.mkdir(exist_ok=True)
    per_agent = {a: load_csv(RUNS / a / "results.csv") for a in agents}
    ids = sorted(set.intersection(*(set(d.keys()) for d in per_agent.values())))

    # write markdown
    lines = ["## Agents comparison (higher is better)\n"]
    header = ["Task"]
    for a in agents:
        header.append(f"{a}:agg")
    for a in agents:
        header.append(f"{a}:correct")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + " --- |" * len(header))

    def val(d, i, k):
        v = d.get(i, {}).get(k)
        try:
            return "" if v is None or v == "" else f"{float(v):.3f}"
        except (TypeError, ValueError):
            return ""

    for tid in ids:
        row = (
            [tid]
            + [val(per_agent[a], tid, "aggregate_score") for a in agents]
            + [val(per_agent[a], tid, "correctness") for a in agents]
        )
        lines.append("| " + " | ".join(row) + " |")

    (REPORTS / "agents_compare.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("Wrote", REPORTS / "agents_compare.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(CONFIG))
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    agents = cfg.get("agents", [])

    for a in agents:
        name = a["name"]
        cmd = a["cmd"]
        # ws = prepare_workspace(name)
        # all_tasks = discover_tasks()
        # for orig in all_tasks:
        #     ws_task = ws / orig.name
        #     run_agent_on_task(cmd, ws_task, orig)
        # score_workspace(name, RUNS / name)

        # ws = prepare_workspace(name)
        # all_tasks = discover_tasks()
        # run_root = RUNS / name
        # for orig in all_tasks:
        #     ws_task = ws / orig.name
        #     run_agent_on_task(cmd, ws_task, orig, run_root)
        # score_workspace(name, run_root)

        ws = prepare_workspace(name)
        all_tasks = discover_tasks()
        run_root = RUNS / name
        for orig in all_tasks:
            ws_task = ws / orig.name
            run_agent_on_task(cmd, ws_task, orig, run_root)
        score_workspace(name, run_root)

    compare_agents([a["name"] for a in agents])


if __name__ == "__main__":
    main()
