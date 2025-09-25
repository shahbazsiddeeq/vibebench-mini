#!/usr/bin/env python3
"""
Merge Python (results.csv) and JS (results_js.csv) into:
- reports/combined_summary.md
- reports/combined_table.md
- reports/combined_aggregate.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
R_PY = ROOT / "results.csv"
R_JS = ROOT / "results_js.csv"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)


def _read(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[df["id"] != "__aggregate__"].copy()
    for c in ("aggregate_score", "correctness"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[["id", "title", "aggregate_score", "correctness"]].rename(
        columns={"aggregate_score": "agg", "correctness": "corr"}
    )


def main():
    if not R_PY.exists() or not R_JS.exists():
        raise SystemExit(
            "Missing results.csv or results_js.csv. Run both runners first."
        )

    py = _read(R_PY).assign(track="python")
    js = _read(R_JS).assign(track="js")

    # Outer-join on task id (some tracks may have different sets)
    merged = pd.merge(py, js, on="id", how="outer", suffixes=("_py", "_js"))
    merged = merged.sort_values("id").reset_index(drop=True)

    # --- chart: aggregate (per task, two bars: Py vs JS) ---
    ids = merged["id"].tolist()
    vals_py = merged["agg_py"].tolist()
    vals_js = merged["agg_js"].tolist()

    x = range(len(ids))
    width = 0.4
    plt.figure(figsize=(12, 6))
    plt.bar([i - width / 2 for i in x], vals_py, width)
    plt.bar([i + width / 2 for i in x], vals_js, width)
    plt.title("Aggregate by task — Python vs JS")
    plt.xlabel("Task")
    plt.ylabel("Aggregate (0–1)")
    plt.xticks(list(x), ids, rotation=0)
    plt.tight_layout()
    plt.savefig(OUT / "combined_aggregate.png", dpi=180)
    plt.close()

    # --- table (markdown) ---
    lines = [
        "| Task | Py agg | JS agg | Py corr | JS corr |",
        "|---|---:|---:|---:|---:|",
    ]

    def fmt(v):
        return "" if pd.isna(v) else f"{float(v):.3f}"

    for _, r in merged.iterrows():
        lines.append(
            f"| {r['id']} | {fmt(r['agg_py'])} | {fmt(r['agg_js'])} | {fmt(r['corr_py'])} | {fmt(r['corr_js'])} |"
        )
    (OUT / "combined_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # --- summary ---
    mean_py = py["agg"].mean()
    mean_js = js["agg"].mean()
    md = [
        "## Cross-track Summary (Python vs JS)\n",
        f"- Python mean aggregate: **{mean_py:.3f}**",
        f"- JS mean aggregate: **{mean_js:.3f}**",
        "",
        "See also:",
        "- `reports/combined_aggregate.png`",
        "- `reports/combined_table.md`",
    ]
    (OUT / "combined_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote combined reports to", OUT)


if __name__ == "__main__":
    main()
