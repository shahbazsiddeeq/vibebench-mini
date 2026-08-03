#!/usr/bin/env python3
"""Contamination and leakage audit for CodeAssay.

Computes, for every CodeAssay task, its maximum normalized character-level
similarity (difflib.SequenceMatcher ratio) against all 1,138 HumanEval and MBPP
tasks, separately for descriptions and for reference solutions.

This supports the narrow claim made in the paper: no evidence of derivation from
HumanEval or MBPP. It concerns construction provenance only and says nothing
about any model's training data.

Reproducibility notes
---------------------
* The two reference corpora are downloaded on first run into ``data/external``
  and their SHA-256 digests are recorded in the output, so a reader can confirm
  they used the same inputs. HumanEval is MIT licensed, MBPP is Apache-2.0.
* Two description variants are reported. ``desc`` parses the title and
  description out of ``task.yaml``; ``desc_raw`` uses the whole ``task.yaml``
  file, which is what an earlier version of this script did. They differ only by
  the two YAML keys.
* Outputs are written to ``reports/`` so the numbers quoted in the paper are
  traceable to a released file.

Usage:  python3 scripts/leakage_check.py [--offline]
"""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks" / "python"
DATA = ROOT / "data" / "external"
REPORTS = ROOT / "reports"

SOURCES = {
    "HumanEval.jsonl": "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz",
    "mbpp.jsonl": "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/mbpp.jsonl",
}

THRESHOLD = 0.70


def fetch(offline: bool) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        dest = DATA / name
        if dest.exists():
            continue
        if offline:
            sys.exit(f"missing {dest} and --offline was given")
        print(f"downloading {name}", file=sys.stderr)
        raw = urllib.request.urlopen(url, timeout=120).read()
        if url.endswith(".gz"):
            import gzip

            raw = gzip.decompress(raw)
        dest.write_bytes(raw)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_codeassay() -> list[tuple[str, str, str, str]]:
    """Return (task_name, description, raw_yaml, reference_solution) per task."""
    out = []
    for d in sorted(TASKS.iterdir()):
        if not (d.is_dir() and d.name.startswith("task")):
            continue
        yaml_path, sol_path = d / "task.yaml", d / "src" / "solution.py"
        raw = yaml_path.read_text() if yaml_path.exists() else ""
        # task.yaml carries only `title:` and `description:`; parse without a
        # yaml dependency so the artifact runs on a bare interpreter.
        fields = []
        for key in ("title:", "description:"):
            for line in raw.splitlines():
                if line.startswith(key):
                    fields.append(line[len(key):].strip())
                    break
        desc = " ".join(fields)
        sol = sol_path.read_text() if sol_path.exists() else ""
        out.append((d.name, desc, raw, sol))
    return out


def load_reference_corpora() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    descs, codes = [], []
    for line in (DATA / "HumanEval.jsonl").read_text().splitlines():
        o = json.loads(line)
        descs.append((o["task_id"], o.get("prompt", "")))
        codes.append((o["task_id"], o.get("prompt", "") + o.get("canonical_solution", "")))
    for line in (DATA / "mbpp.jsonl").read_text().splitlines():
        o = json.loads(line)
        tid = "mbpp/" + str(o.get("task_id"))
        descs.append((tid, o.get("text", "")))
        codes.append((tid, o.get("code", "")))
    return descs, codes


def norm(s: str) -> str:
    return " ".join(s.lower().split())


def best_match(query: str, pool: list[tuple[str, str]]) -> tuple[float, str | None]:
    """Max SequenceMatcher ratio of query against any pool item, quick_ratio pruned."""
    sm = difflib.SequenceMatcher()
    sm.set_seq2(norm(query))
    best, best_id = 0.0, None
    for pid, ptext in pool:
        sm.set_seq1(norm(ptext))
        if sm.quick_ratio() <= best:  # valid upper bound, safe to prune
            continue
        r = sm.ratio()
        if r > best:
            best, best_id = r, pid
    return best, best_id


def summarize(vals: list[float], label: str, lines: list[str]) -> None:
    ordered = sorted(vals, reverse=True)
    lines.append(f"\n### {label}")
    lines.append(
        f"max {max(vals):.3f} | mean {sum(vals) / len(vals):.3f} | "
        f"median {ordered[len(ordered) // 2]:.3f}"
    )
    for th in (0.80, 0.70, 0.60, 0.50):
        lines.append(f"- above {th:.2f}: {sum(1 for v in vals if v > th)} tasks")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="fail rather than download")
    args = ap.parse_args()

    fetch(args.offline)
    REPORTS.mkdir(exist_ok=True)

    tasks = load_codeassay()
    pool_desc, pool_code = load_reference_corpora()
    print(
        f"CodeAssay tasks: {len(tasks)}; reference items: {len(pool_desc)}",
        file=sys.stderr,
    )

    rows = []
    for i, (name, desc, raw, sol) in enumerate(tasks, 1):
        d_max, d_id = best_match(desc, pool_desc)
        r_max, _ = best_match(raw, pool_desc)
        s_max, s_id = best_match(sol, pool_code)
        rows.append(
            {
                "task": name,
                "desc_max": round(d_max, 4),
                "desc_nearest": d_id,
                "desc_raw_max": round(r_max, 4),
                "solution_max": round(s_max, 4),
                "solution_nearest": s_id,
            }
        )
        print(f"[{i}/{len(tasks)}] {name} desc={d_max:.3f} sol={s_max:.3f}", file=sys.stderr)

    csv_path = REPORTS / "leakage_similarity.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    d_vals = [r["desc_max"] for r in rows]
    r_vals = [r["desc_raw_max"] for r in rows]
    s_vals = [r["solution_max"] for r in rows]

    lines = [
        "# Contamination and leakage audit",
        "",
        f"CodeAssay tasks: {len(tasks)}. Reference corpus: {len(pool_desc)} tasks "
        f"(HumanEval 164 + MBPP 974).",
        "Metric: maximum normalized character-level SequenceMatcher ratio against "
        "any reference task.",
        f"Candidate-overlap threshold: {THRESHOLD:.2f}.",
        "",
        "## Input digests (SHA-256)",
    ]
    for name in SOURCES:
        lines.append(f"- `{name}`: `{digest(DATA / name)}`")

    summarize(d_vals, "Descriptions (title + description)", lines)
    summarize(r_vals, "Descriptions (whole task.yaml, earlier method)", lines)
    summarize(s_vals, "Reference solutions", lines)

    over = [r for r in rows if max(r["desc_max"], r["solution_max"]) > THRESHOLD]
    lines.append(
        f"\n### Pairs above the {THRESHOLD:.2f} threshold: {len(over)}"
        + ("" if over else " (none)")
    )
    top_d = sorted(rows, key=lambda r: -r["desc_max"])[:5]
    top_s = sorted(rows, key=lambda r: -r["solution_max"])[:5]
    lines.append("\n### Five most similar descriptions")
    for r in top_d:
        lines.append(f"- {r['task']}: {r['desc_max']:.3f} vs {r['desc_nearest']}")
    lines.append("\n### Five most similar solutions")
    for r in top_s:
        lines.append(f"- {r['task']}: {r['solution_max']:.3f} vs {r['solution_nearest']}")
    lines.append(f"\nPer-task values: `reports/{csv_path.name}`.")

    md = "\n".join(lines) + "\n"
    (REPORTS / "leakage_summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
