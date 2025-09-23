#!/usr/bin/env python3
"""
Reads results.csv and writes:
- reports/aggregate_bar.png
- reports/correctness_bar.png
- reports/subscores_bar__{complexity,lint,security,deps,mutation}.png
- reports/summary.csv (mean of metrics)
- reports/summary.md  (markdown snippet for your paper/README)
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "results.csv"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)


def _load():
    df = pd.read_csv(CSV)
    # drop the aggregate footer row if present
    df = df[df["id"] != "__aggregate__"].copy()
    # cast numeric columns
    numeric = [
        "tests_total",
        "tests_passed",
        "tests_failed",
        "tests_errors",
        "correctness",
        "complexity_avg",
        "complexity_score",
        "lint_issues",
        "lint_score",
        "security_issues",
        "security_score",
        "dep_vulns",
        "dep_score",
        "mutation_killed",
        "mutation_total",
        "mutation_score",
        "aggregate_score",
    ]
    for c in numeric:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # nice sort by task id then title
    df = df.sort_values(["id"]).reset_index(drop=True)
    return df


def _bar(df, col, fname, ylabel=None):
    plt.figure(figsize=(10, 5))
    plt.bar(df["id"], df[col])
    plt.title(col.replace("_", " ").title())
    plt.xlabel("Task")
    plt.ylabel(ylabel or col)
    plt.tight_layout()
    plt.savefig(OUT / fname, dpi=180)
    plt.close()


def main():
    df = _load()

    # --- charts ---
    if "aggregate_score" in df:
        _bar(df, "aggregate_score", "aggregate_bar.png", "Aggregate score (0–1)")

    if "correctness" in df:
        _bar(df, "correctness", "correctness_bar.png", "Correctness (0–1)")

    # subscores (create separate charts, one per metric)
    if "complexity_score" in df:
        _bar(
            df,
            "complexity_score",
            "subscores_bar__complexity.png",
            "Complexity score (0–1)",
        )
    if "lint_score" in df:
        _bar(df, "lint_score", "subscores_bar__lint.png", "Lint score (0–1)")
    if "security_score" in df:
        _bar(
            df, "security_score", "subscores_bar__security.png", "Security score (0–1)"
        )
    if "dep_score" in df:
        _bar(df, "dep_score", "subscores_bar__deps.png", "Dependency score (0–1)")
    if "mutation_score" in df and not df["mutation_score"].isna().all():
        _bar(
            df, "mutation_score", "subscores_bar__mutation.png", "Mutation score (0–1)"
        )

    # --- summary table (means) ---
    means = {
        "num_tasks": len(df),
        "mean_aggregate": df["aggregate_score"].mean(),
        "mean_correctness": df["correctness"].mean(),
        "mean_complexity": df.get("complexity_score", pd.Series(dtype=float)).mean(),
        "mean_lint": df.get("lint_score", pd.Series(dtype=float)).mean(),
        "mean_security": df.get("security_score", pd.Series(dtype=float)).mean(),
        "mean_deps": df.get("dep_score", pd.Series(dtype=float)).mean(),
        "mean_mutation": df.get("mutation_score", pd.Series(dtype=float)).mean(),
    }
    pd.DataFrame([means]).to_csv(OUT / "summary.csv", index=False)

    # markdown snippet for your paper/README
    md = [
        "## VibeBench-Mini — Results Summary\n",
        f"- Tasks evaluated: **{means['num_tasks']}**",
        f"- Mean aggregate: **{means['mean_aggregate']:.3f}**",
        f"- Mean correctness: **{means['mean_correctness']:.3f}**",
    ]
    if pd.notna(means["mean_mutation"]):
        md.append(f"- Mean mutation score: **{means['mean_mutation']:.3f}**")
    md.extend(
        [
            "",
            "### Charts",
            "- `reports/aggregate_bar.png`",
            "- `reports/correctness_bar.png`",
            "- `reports/subscores_bar__*.png`",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(md), encoding="utf-8")
    print("Wrote charts + tables to", OUT)


if __name__ == "__main__":
    main()
