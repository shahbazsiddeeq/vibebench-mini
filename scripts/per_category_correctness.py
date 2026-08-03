#!/usr/bin/env python3
"""Per-category hidden-test correctness for every model and prompt configuration.

The paper reports only the range of category means and the widest and narrowest
between-model spreads. This writes the full matrix so the per-category values are
checkable rather than asserted.

Source of truth is the `final_hidden_pass` column of `reports/r2_repair_audit.csv`,
the same column the main statistics use, so these numbers cannot drift from the
reported correctness.

Outputs
-------
reports/per_category_correctness.csv   one row per configuration and category
reports/per_category_correctness.md    the standard-prompt summary quoted in RQ3
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports" / "r2_repair_audit.csv"
CATS = ROOT / "tasks" / "categories.json"
REPORTS = ROOT / "reports"

# categories.json stores the abbreviation; this gives the full name used in the
# paper's Table 1 so the released file is readable on its own.
FULL_NAME = {
    "ADS": "Algorithms & Data Structures",
    "SPT": "String & Text Processing",
    "DPS": "Data Processing & Statistics",
    "FIO": "File I/O & System",
    "WNT": "Web & Networking",
    "CCA": "Concurrency & Async",
    "CAT": "Crypto, Auth & Tokens",
    "DBS": "Database & Storage",
    "TCQ": "Testing & Code Quality",
    "ODP": "OOP & Design Patterns",
}


def load_categories() -> dict[str, str]:
    raw = json.loads(CATS.read_text())
    out: dict[str, str] = {}
    for k, v in raw.items():
        if isinstance(v, str):
            out[k] = v
        elif isinstance(v, list):
            for t in v:
                out[t] = k
    return out


def main() -> None:
    cat_of = load_categories()
    rows = list(csv.DictReader(AUDIT.open()))
    if not rows:
        raise SystemExit(f"no rows in {AUDIT}")

    # (run, category) -> [n, n_correct]
    acc: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
    meta: dict[str, tuple[str, str]] = {}
    for r in rows:
        cat = cat_of.get(r["task"])
        if cat is None:
            continue
        run = r["run"]
        meta[run] = (r["model_label"], r["prompt"])
        a = acc[(run, cat)]
        a[0] += 1
        a[1] += r["final_hidden_pass"] == "True"

    cats = sorted({c for _, c in acc}, key=lambda c: -sum(
        acc[(run, c)][0] for run in meta if (run, c) in acc))
    runs = sorted(meta)

    out_rows = []
    for run in runs:
        model, prompt = meta[run]
        for cat in cats:
            n, k = acc.get((run, cat), (0, 0))
            if not n:
                continue
            out_rows.append({
                "run": run,
                "model": model,
                "prompt": prompt,
                "abbr": cat,
                "category": FULL_NAME.get(cat, cat),
                "n_tasks": n,
                "n_correct": k,
                "correctness_pct": round(100 * k / n, 1),
            })

    csv_path = REPORTS / "per_category_correctness.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)

    # Standard-prompt summary, the view RQ3 quotes.
    std = [r for r in out_rows if r["prompt"] == "std"]
    n_models = len({r["run"] for r in std})
    lines = [
        "# Per-category correctness",
        "",
        f"Source: `reports/{AUDIT.name}`, column `final_hidden_pass`. "
        f"{len(runs)} configurations, {len(cats)} categories.",
        f"Per-configuration values: `reports/{csv_path.name}`.",
        "",
        f"## Standard prompt ({n_models} models)",
        "",
        "| Abbr. | Category | #Tasks | Mean (%) | Min (%) | Max (%) | Spread |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    summary = []
    for cat in cats:
        vals = [r["correctness_pct"] for r in std if r["abbr"] == cat]
        if not vals:
            continue
        n = next(r["n_tasks"] for r in std if r["abbr"] == cat)
        mean = sum(vals) / len(vals)
        summary.append((cat, n, mean, min(vals), max(vals)))
    for cat, n, mean, lo, hi in sorted(summary, key=lambda r: r[4] - r[3], reverse=True):
        lines.append(
            f"| {cat} | {FULL_NAME.get(cat, cat)} | {n} | {mean:.1f} | {lo:.1f} | {hi:.1f} "
            f"| {hi-lo:.1f} |"
        )
    means = [s[2] for s in summary]
    spreads = [s[4] - s[3] for s in summary]
    lines += [
        "",
        f"Category means range {min(means):.1f} to {max(means):.1f}. "
        f"Spreads range {min(spreads):.1f} to {max(spreads):.1f}.",
        f"Categories in which some model scores 100 percent: "
        f"{sum(1 for s in summary if s[4] == 100.0)} of {len(summary)}.",
    ]
    md = "\n".join(lines) + "\n"
    (REPORTS / "per_category_correctness.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
