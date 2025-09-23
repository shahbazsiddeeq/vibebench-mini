#!/usr/bin/env python3
"""
Summarize .agent_runs/* results into:
- reports/agents_summary.md (markdown table, ranked)
- reports/agents_summary.csv (CSV)
Picks 'copyref' as baseline if present; otherwise the first agent found.
"""

from __future__ import annotations

import csv
import json
import math
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / ".agent_runs"
REPORTS = ROOT / "reports"


def load_agent_rows(agent: str) -> dict[str, dict]:
    """Return task_id -> metric dict from results.csv (skip __aggregate__)."""
    path = RUNS / agent / "results.csv"
    rows: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("id") == "__aggregate__":
                continue
            rows[r["id"]] = r
    # coerce numeric fields
    for r in rows.values():
        for k, v in list(r.items()):
            if k == "id":
                continue
            try:
                r[k] = float(v) if v not in ("", None) else None
            except (TypeError, ValueError):
                r[k] = None
    return rows


def load_agent_aggregate(agent: str) -> tuple[int, float]:
    """(num_tasks, aggregate_score) from results.json (fallback to CSV)."""
    j = RUNS / agent / "results.json"
    if j.exists():
        data = json.loads(j.read_text(encoding="utf-8"))
        n = len(data.get("tasks", []))
        agg = float(data.get("aggregate", {}).get("mean_score", 0.0))
        return n, agg
    # fallback to CSV aggregate row if JSON missing
    c = RUNS / agent / "results.csv"
    with c.open(encoding="utf-8") as f:
        agg_row = None
        for r in csv.DictReader(f):
            if r.get("id") == "__aggregate__":
                agg_row = r
                break
    agg = float(agg_row["aggregate_score"]) if agg_row else 0.0
    # count tasks by scanning directory
    tdir = RUNS / agent / "tasks" / "python"
    n = len([p for p in tdir.iterdir() if p.is_dir()]) if tdir.exists() else 0
    return n, agg


def mean_correctness(rows: dict[str, dict]) -> float | None:
    vals = [
        r.get("correctness") for r in rows.values() if r.get("correctness") is not None
    ]
    if not vals:
        return None
    try:
        return st.mean(vals)
    except st.StatisticsError:
        return None


def summarize_agent(agent: str) -> dict:
    rows = load_agent_rows(agent)
    n_tasks, agg = load_agent_aggregate(agent)
    mc = mean_correctness(rows)
    return {
        "agent": agent,
        "num_tasks": n_tasks or len(rows),
        "aggregate_score": agg,
        "mean_correctness": None if mc is None else mc,
    }


def pick_baseline(agents: list[str]) -> str:
    return "copyref" if "copyref" in agents else agents[0]


def fmtf(v: float | None, places: int = 3) -> str:
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "—"
    return f"{v:.{places}f}"


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    agents = (
        sorted([p.name for p in RUNS.iterdir() if (p / "results.csv").exists()])
        if RUNS.exists()
        else []
    )
    if not agents:
        raise SystemExit("No agents found under .agent_runs/. Run agents first.")

    baseline = pick_baseline(agents)
    data = [summarize_agent(a) for a in agents]
    # rank by aggregate_score desc
    data.sort(key=lambda d: d["aggregate_score"], reverse=True)
    base_agg = next(
        (d["aggregate_score"] for d in data if d["agent"] == baseline), None
    )

    # write CSV
    csv_path = REPORTS / "agents_summary.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank",
                "agent",
                "num_tasks",
                "aggregate_score",
                "mean_correctness",
                "delta_vs_baseline",
            ]
        )
        for i, d in enumerate(data, start=1):
            delta = None if base_agg is None else d["aggregate_score"] - base_agg
            w.writerow(
                [
                    i,
                    d["agent"],
                    d["num_tasks"],
                    fmtf(d["aggregate_score"]),
                    fmtf(d["mean_correctness"]),
                    fmtf(delta),
                ]
            )

    # write Markdown
    lines = [
        "## Agents Summary (ranked by aggregate score)\n",
        f"**Baseline:** `{baseline}`\n",
        "| # | Agent | Tasks | Aggregate | Mean Correctness | Δ vs Baseline |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for i, d in enumerate(data, start=1):
        delta = None if base_agg is None else d["aggregate_score"] - base_agg
        lines.append(
            f"| {i} | `{d['agent']}` | {d['num_tasks']} | "
            f"{fmtf(d['aggregate_score'])} | {fmtf(d['mean_correctness'])} | {fmtf(delta)} |"
        )
    md_path = REPORTS / "agents_summary.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Wrote", md_path, "and", csv_path)


if __name__ == "__main__":
    main()
