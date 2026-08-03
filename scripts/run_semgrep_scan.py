#!/usr/bin/env python3.12
"""Semgrep scan of every generated solution and of the reference solutions.

The runner has an optional Semgrep hook,
but Semgrep was never installed and never run, so the paper reported Bandit
only. This script produces the missing evidence: it scans all 14 configurations'
generated solutions plus the 185 reference solutions with two published
rulesets, and reports per-configuration finding counts by severity and rule.

Rulesets:
  p/python          the Semgrep Registry Python pack (correctness and security)
  p/security-audit  the Registry security-audit pack (security patterns only)

Outputs:
  reports/semgrep_findings.csv     one row per finding
  reports/semgrep_summary.md       per-configuration counts and top rules

Run:  python3.12 scripts/run_semgrep_scan.py
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / ".agent_runs"
REPORTS = ROOT / "reports"
TASKS = ROOT / "tasks" / "python"
# The staging directory must sit OUTSIDE the repository. Semgrep skips
# dot-directories and also honours .gitignore, and `.semgrep_scratch/` is listed
# in this repository's .gitignore, so staging in place silently scanned zero
# files. Every scan asserts its file count against the number staged.
SCRATCH = Path(tempfile.mkdtemp(prefix="codeassay_semgrep_"))

SEMGREP = ROOT / ".venv" / "bin" / "semgrep"
RULESETS = ["p/python", "p/security-audit"]

MODELS = [
    ("gpt4omini", "GPT-4o-mini"),
    ("gpt4o", "GPT-4o"),
    ("gpt56sol", "GPT-5.6-sol"),
    ("haiku45", "Claude Haiku 4.5"),
    ("sonnet45", "Claude Sonnet 4.5"),
    ("sonnet5", "Claude Sonnet 5"),
    ("gemini25", "Gemini 2.5 Flash"),
]
PROMPTS = ["std", "sec"]


def semgrep_bin() -> str:
    if SEMGREP.exists():
        return str(SEMGREP)
    found = shutil.which("semgrep")
    if not found:
        sys.exit("semgrep not found; pip install semgrep")
    return found


def scan(directory: Path, ruleset: str) -> tuple[list[dict], int]:
    """Run one ruleset over a directory. Returns (findings, files_scanned)."""
    proc = subprocess.run(
        [semgrep_bin(), "--quiet", "--json", "--config", ruleset, str(directory)],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"  ! semgrep produced no JSON for {directory.name}/{ruleset}")
        print(f"    {proc.stderr[:300]}")
        return [], 0
    scanned = len(data.get("paths", {}).get("scanned", []))
    out = []
    for r in data.get("results", []):
        out.append(
            {
                "file": Path(r.get("path", "")).name,
                "check_id": r.get("check_id", ""),
                "severity": r.get("extra", {}).get("severity", ""),
                "message": " ".join(
                    (r.get("extra", {}).get("message", "") or "").split()
                )[:200],
            }
        )
    return out, scanned


def stage_cache(slug: str, prompt: str) -> Path | None:
    """Copy a run's cached solutions into a non-hidden directory.

    Semgrep skips dot-directories by default, and the runs live under
    `.agent_runs`, so scanning them in place silently reports zero files. The
    solutions are staged out before scanning and the file count is asserted
    against the number staged.
    """
    cache = RUNS / f"{slug}-{prompt}" / "cache"
    if not cache.exists():
        return None
    dest = SCRATCH / f"{slug}-{prompt}"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    n = 0
    for f in sorted(cache.glob("*.py")):
        shutil.copy(f, dest / f.name)
        n += 1
    if n == 0:
        return None
    return dest


def stage_reference() -> Path:
    """Copy the 185 reference solutions into a flat directory for scanning."""
    dest = SCRATCH / "reference"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    n = 0
    for task in sorted(TASKS.glob("task*")):
        src = task / "src" / "solution.py"
        if src.exists():
            shutil.copy(src, dest / f"{task.name}.py")
            n += 1
    print(f"staged {n} reference solutions")
    return dest


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    SCRATCH.mkdir(exist_ok=True)

    targets: list[tuple[str, str, Path]] = []
    for slug, name in MODELS:
        for prompt in PROMPTS:
            staged = stage_cache(slug, prompt)
            if staged is None:
                print(f"! missing or empty cache for {slug}-{prompt}")
                continue
            n = len(list(staged.glob("*.py")))
            print(f"staged {n} solutions for {slug}-{prompt}")
            targets.append((name, prompt, staged))
    targets.append(("CodeAssay reference", "n/a", stage_reference()))

    rows: list[dict] = []
    summary: dict[tuple[str, str, str], dict] = {}

    for name, prompt, directory in targets:
        for ruleset in RULESETS:
            print(f"scanning {name} [{prompt}] with {ruleset} ...", flush=True)
            findings, scanned = scan(directory, ruleset)
            staged = len(list(directory.glob("*.py")))
            if scanned != staged:
                sys.exit(
                    f"semgrep scanned {scanned} of {staged} staged files in "
                    f"{directory}; refusing to report a partial scan"
                )
            sev = Counter(f["severity"] for f in findings)
            summary[(name, prompt, ruleset)] = {
                "files": scanned,
                "total": len(findings),
                "files_with_findings": len({f["file"] for f in findings}),
                "ERROR": sev.get("ERROR", 0),
                "WARNING": sev.get("WARNING", 0),
                "INFO": sev.get("INFO", 0),
                "rules": Counter(f["check_id"] for f in findings),
            }
            for f in findings:
                rows.append(
                    {
                        "configuration": name,
                        "prompt": prompt,
                        "ruleset": ruleset,
                        **f,
                    }
                )

    fields = ["configuration", "prompt", "ruleset", "file", "check_id", "severity", "message"]
    with (REPORTS / "semgrep_findings.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=fields)
        wr.writeheader()
        wr.writerows(rows)

    L = ["# Semgrep scan of generated and reference solutions", ""]
    L.append(
        "Produced by `scripts/run_semgrep_scan.py`. Semgrep "
        f"{subprocess.run([semgrep_bin(), '--version'], capture_output=True, text=True).stdout.strip()}. "
        "Rulesets are the published Semgrep Registry packs `p/python` and "
        "`p/security-audit`, used at their default severities with no local "
        "rule additions or suppressions."
    )
    L.append("")
    for ruleset in RULESETS:
        L.append(f"## Ruleset `{ruleset}`")
        L.append("")
        L.append("| Configuration | Prompt | Files | Findings | Files w/ findings | ERROR | WARNING | INFO |")
        L.append("|---|---|---|---|---|---|---|---|")
        for (name, prompt, rs), s in summary.items():
            if rs != ruleset:
                continue
            L.append(
                f"| {name} | {prompt} | {s['files']} | {s['total']} | "
                f"{s['files_with_findings']} | {s['ERROR']} | {s['WARNING']} | {s['INFO']} |"
            )
        L.append("")
        agg: Counter = Counter()
        for (name, prompt, rs), s in summary.items():
            if rs == ruleset:
                agg.update(s["rules"])
        if agg:
            L.append("Most frequent rules across all configurations:")
            L.append("")
            L.append("| Rule | Hits |")
            L.append("|---|---|")
            for rule, cnt in agg.most_common(15):
                L.append(f"| `{rule}` | {cnt} |")
        else:
            L.append("No findings from this ruleset on any configuration.")
        L.append("")

    (REPORTS / "semgrep_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\nwrote {REPORTS / 'semgrep_summary.md'}")
    print(f"wrote {REPORTS / 'semgrep_findings.csv'}  ({len(rows)} findings)")


if __name__ == "__main__":
    main()
