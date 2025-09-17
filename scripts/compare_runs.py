#!/usr/bin/env python3
"""
Compare two results.csv files (A vs B) and write:
- reports/diff.csv
- reports/diff.md (markdown table)
If --a/--b not given, uses the last two entries in history/index.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)


def load_csv(p: Path) -> pd.DataFrame:
    df = pd.read_csv(p)
    return df[df["id"] != "__aggregate__"].copy()


def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if c == "id":
            continue
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def latest_two_from_history() -> tuple[Path, Path]:
    idx = ROOT / "history" / "index.json"
    if not idx.exists():
        raise SystemExit(
            "No history/index.json found. Run `make archive` twice to create two runs."
        )
    entries = json.loads(idx.read_text(encoding="utf-8"))
    if len(entries) < 2:
        raise SystemExit(
            "Need at least two archived runs. Run `make archive` again after another benchmark."
        )
    a = ROOT / entries[-2]["path"] / "results.csv"
    b = ROOT / entries[-1]["path"] / "results.csv"
    return a, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=Path, help="results.csv (baseline)")
    ap.add_argument("--b", type=Path, help="results.csv (new)")
    args = ap.parse_args()

    a_path, b_path = (args.a, args.b)
    if a_path is None or b_path is None:
        a_path, b_path = latest_two_from_history()

    a = coerce_numeric(load_csv(a_path)).set_index("id")
    b = coerce_numeric(load_csv(b_path)).set_index("id")

    # intersect columns & tasks
    cols = [c for c in a.columns if c in b.columns and c != "title"]
    ids = sorted(set(a.index) & set(b.index))
    a, b = a.loc[ids, cols], b.loc[ids, cols]
    diff = (b - a).round(3)
    diff.insert(0, "metric", [*cols])  # not used but handy when melting

    # write CSV
    out_csv = OUT / "diff.csv"
    diff.to_csv(out_csv)

    # write Markdown (aggregate + key metrics)
    show = [
        "aggregate_score",
        "correctness",
        "lint_score",
        "security_score",
        "dep_score",
    ]
    present = [c for c in show if c in diff.columns]
    lines = ["## Run-to-Run Diff (B - A)\n", f"**A:** {a_path}", f"**B:** {b_path}", ""]
    header = "| Task | " + " | ".join(present) + " |"
    sep = "|" + " --- |" * (len(present) + 1)
    lines += [header, sep]
    for tid in ids:
        row = [tid] + [
            f"{diff.loc[tid, c]:+.3f}" if pd.notna(diff.loc[tid, c]) else ""
            for c in present
        ]
        lines.append("| " + " | ".join(row) + " |")
    (OUT / "diff.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote:", out_csv, "and", OUT / "diff.md")


if __name__ == "__main__":
    main()
