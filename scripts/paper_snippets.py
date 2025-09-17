#!/usr/bin/env python3
"""
Generate paper-ready tables/snippets from results.csv:
- reports/table.tex     (LaTeX table of per-task metrics)
- reports/table.md      (Markdown table)
- reports/metrics.tex   (LaTeX macros with mean scores)
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "results.csv"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)


def load_df():
    df = pd.read_csv(CSV)
    df = df[df["id"] != "__aggregate__"].copy()
    # numeric columns
    num = [
        "correctness",
        "complexity_score",
        "lint_score",
        "security_score",
        "dep_score",
        "mutation_score",
        "aggregate_score",
    ]
    for c in num:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.sort_values("id").reset_index(drop=True)


def latex_escape(s: str) -> str:
    return (
        s.replace("_", r"\_")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("#", r"\#")
    )


def write_latex_table(df: pd.DataFrame, path: Path, topn: int | None = None):
    cols = [
        "id",
        "correctness",
        "complexity_score",
        "lint_score",
        "security_score",
        "dep_score",
        "aggregate_score",
    ]
    use = [c for c in cols if c in df.columns]
    d = df[use].copy()
    if topn:
        d = d.sort_values("aggregate_score", ascending=False).head(topn)
    # round for display
    for c in d.columns:
        if c != "id":
            d[c] = d[c].map(lambda x: "" if pd.isna(x) else f"{x:.3f}")
    # build LaTeX
    header = r"\begin{tabular}{l" + "r" * (len(d.columns) - 1) + "}\n\\toprule\n"
    colnames = [
        "Task",
        "Correct",
        "Complexity",
        "Lint",
        "Security",
        "Deps",
        "Aggregate",
    ]
    colnames = colnames[: len(d.columns)]
    body = " & ".join(colnames) + r" \\" + "\n\\midrule\n"
    for _, row in d.iterrows():
        cells = [latex_escape(str(row[k])) for k in d.columns]
        body += " & ".join(cells) + r" \\" + "\n"
    footer = r"\bottomrule" + "\n" + r"\end{tabular}" + "\n"
    path.write_text(header + body + footer, encoding="utf-8")


def write_markdown_table(df: pd.DataFrame, path: Path):
    cols = [
        "id",
        "correctness",
        "complexity_score",
        "lint_score",
        "security_score",
        "dep_score",
        "aggregate_score",
    ]
    use = [c for c in cols if c in df.columns]
    d = df[use].copy()
    for c in d.columns:
        if c != "id":
            d[c] = d[c].map(lambda x: "" if pd.isna(x) else f"{x:.3f}")
    lines = [
        "| Task | Correct | Complexity | Lint | Security | Deps | Aggregate |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for _, r in d.iterrows():
        vals = [
            str(r.get("id", "")),
            r.get("correctness", ""),
            r.get("complexity_score", ""),
            r.get("lint_score", ""),
            r.get("security_score", ""),
            r.get("dep_score", ""),
            r.get("aggregate_score", ""),
        ]
        lines.append("| " + " | ".join(vals) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_metrics_macros(df: pd.DataFrame, path: Path):
    means = {
        "meanAggregate": df["aggregate_score"].mean(),
        "meanCorrect": df["correctness"].mean(),
        "meanComplex": df.get("complexity_score").mean(),
        "meanLint": df.get("lint_score").mean(),
        "meanSecurity": df.get("security_score").mean(),
        "meanDeps": df.get("dep_score").mean(),
        "meanMutation": (
            df.get("mutation_score").mean() if "mutation_score" in df else float("nan")
        ),
    }

    def fmt(v):
        return "" if pd.isna(v) else f"{v:.3f}"

    tex = "\n".join([f"\\newcommand\\{k}{{{fmt(v)}}}" for k, v in means.items()]) + "\n"
    path.write_text(tex, encoding="utf-8")


def main():
    df = load_df()
    write_latex_table(df, OUT / "table.tex")
    write_markdown_table(df, OUT / "table.md")
    write_metrics_macros(df, OUT / "metrics.tex")
    print("Wrote:", OUT / "table.tex", OUT / "table.md", OUT / "metrics.tex")


if __name__ == "__main__":
    main()
