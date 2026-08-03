#!/usr/bin/env python3
"""Aggregate the PROFES-revision per-config results (hidden-test grading).

Scans .agent_runs/<model>-<std|sec>/results.csv for the 7 rev models and reports:
  pass@1 (fraction passing ALL hidden tests), mean correctness, and — among the
  all-hidden-pass solutions only (strict gate) — mean quality indicators.

Usage: python scripts/agg_rev.py [--csv out.csv]
"""
import argparse
import csv
import glob
import os
import statistics as st

MODELS = ["gpt4omini", "gpt4o", "gpt56sol", "haiku45", "sonnet45", "sonnet5", "gemini25"]
QUAL = ["complexity_score", "lint_score", "security_score"]


def load(name):
    f = f".agent_runs/{name}/results.csv"
    if not os.path.exists(f):
        return None
    rows = [r for r in csv.DictReader(open(f)) if r.get("id") != "__aggregate__"]
    return rows or None


def fnum(r, k):
    v = r.get(k)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def summarize(rows):
    corr = [fnum(r, "correctness") for r in rows]
    corr = [c for c in corr if c is not None]
    passers = [r for r in rows if fnum(r, "correctness") == 1.0]
    out = {
        "n": len(rows),
        "pass@1": len(passers),
        "pass@1_pct": round(100 * len(passers) / max(1, len(corr)), 1),
        "mean_corr": round(st.mean(corr), 3) if corr else None,
        "n_pass": len(passers),
    }
    for q in QUAL:
        vals = [fnum(r, q) for r in passers]
        vals = [v for v in vals if v is not None]
        out[q] = round(st.mean(vals), 3) if vals else None
    agg = [fnum(r, "aggregate_score") for r in passers]
    agg = [a for a in agg if a is not None]
    out["mean_aggregate_passers"] = round(st.mean(agg), 3) if agg else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()
    hdr = ["config", "n", "pass@1", "pass@1_pct", "mean_corr", "n_pass",
           "complexity_score", "lint_score", "security_score", "mean_aggregate_passers"]
    print(f"{'config':16} {'n':>3} {'pass@1':>6} {'%':>5} {'corr':>5} "
          f"{'cplx':>5} {'style':>5} {'sec':>5} {'aggP':>5}")
    table = []
    done = 0
    for m in MODELS:
        for v in ("std", "sec"):
            name = f"{m}-{v}"
            rows = load(name)
            if rows is None:
                print(f"{name:16}  (no results yet)")
                continue
            done += 1
            s = summarize(rows)
            table.append({"config": name, **s})
            print(f"{name:16} {s['n']:>3} {s['pass@1']:>6} {s['pass@1_pct']:>5} "
                  f"{s['mean_corr'] or 0:>5} {s['complexity_score'] or 0:>5} "
                  f"{s['lint_score'] or 0:>5} {s['security_score'] or 0:>5} "
                  f"{s['mean_aggregate_passers'] or 0:>5}")
    print(f"\n{done}/14 configs done.")
    if args.csv and table:
        with open(args.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=hdr)
            w.writeheader()
            w.writerows(table)
        print("wrote", args.csv)


if __name__ == "__main__":
    main()
