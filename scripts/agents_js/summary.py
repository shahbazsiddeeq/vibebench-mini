#!/usr/bin/env python3
import csv
import math
from pathlib import Path

ROOT = Path(".agent_runs/js/openai-default")
CSV = ROOT / "results.csv"

if not CSV.exists():
    print("No JS agent results yet. Run: make agents-js")
    raise SystemExit(0)

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))


def tofloat(x: str) -> float:
    try:
        return float(x)
    except Exception:
        return float("nan")


def mean_safe(vals):
    vals = [v for v in vals if not math.isnan(v)]
    return float("nan") if not vals else sum(vals) / len(vals)


agg_vals = [tofloat(r.get("aggregate_score", "")) for r in rows]
corr_vals = [tofloat(r.get("correctness", "")) for r in rows]

m_agg = mean_safe(agg_vals)
m_corr = mean_safe(corr_vals)

agg_str = f"{m_agg:.3f}" if not math.isnan(m_agg) else "NA"
corr_str = f"{m_corr:.3f}" if not math.isnan(m_corr) else "NA"

print(f"Tasks: {len(rows)}  Mean aggregate: {agg_str}  Mean correctness: {corr_str}")
