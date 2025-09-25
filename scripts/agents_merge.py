#!/usr/bin/env python3
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

PY = ROOT / ".agent_runs/openai-default/results.csv"
JS = ROOT / ".agent_runs/js/openai-default/results.csv"


def _load(csv_path: Path, tag: str) -> pd.DataFrame:
    if not csv_path.exists():
        return pd.DataFrame(columns=["id", f"agg_{tag}", f"corr_{tag}"])
    df = pd.read_csv(csv_path)
    df = df[df["id"] != "__aggregate__"].copy()
    for col in ("aggregate_score", "correctness"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[["id", "aggregate_score", "correctness"]].rename(
        columns={"aggregate_score": f"agg_{tag}", "correctness": f"corr_{tag}"}
    )


def mean_safe(series):
    vals = [x for x in series if isinstance(x, (int, float)) and not math.isnan(x)]
    return float("nan") if not vals else sum(vals) / len(vals)


def fmt(x):
    return "" if pd.isna(x) else f"{float(x):.3f}"


def main():
    py = _load(PY, "py")
    js = _load(JS, "js")
    if py.empty and js.empty:
        print("No agent results found. Run your agents first.")
        return

    m = pd.merge(py, js, on="id", how="outer").sort_values("id").reset_index(drop=True)

    # Markdown table
    lines = [
        "## Agents — Python vs JS\n",
        "| Task | Py agg | JS agg | Py corr | JS corr |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, r in m.iterrows():
        lines.append(
            f"| {r['id']} | {fmt(r.get('agg_py'))} | {fmt(r.get('agg_js'))} | "
            f"{fmt(r.get('corr_py'))} | {fmt(r.get('corr_js'))} |"
        )

    # Means row
    mean_py_agg = mean_safe(m.get("agg_py", pd.Series(dtype=float)))
    mean_js_agg = mean_safe(m.get("agg_js", pd.Series(dtype=float)))
    mean_py_corr = mean_safe(m.get("corr_py", pd.Series(dtype=float)))
    mean_js_corr = mean_safe(m.get("corr_js", pd.Series(dtype=float)))

    lines += [
        "",
        f"- **Mean agg (Py):** {fmt(mean_py_agg)}",
        f"- **Mean agg (JS):** {fmt(mean_js_agg)}",
        f"- **Mean corr (Py):** {fmt(mean_py_corr)}",
        f"- **Mean corr (JS):** {fmt(mean_js_corr)}",
        "",
        "_Files used_:",
        f"- `{PY.relative_to(ROOT)}` (if present)",
        f"- `{JS.relative_to(ROOT)}` (if present)",
    ]

    (OUT / "agents_combined.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote", OUT / "agents_combined.md")


if __name__ == "__main__":
    main()
