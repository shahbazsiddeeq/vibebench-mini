#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import mean

# Optional imports
try:
    from radon.complexity import cc_visit
except Exception:
    cc_visit = None

try:
    from flake8.api import legacy as flake8_api
except Exception:
    flake8_api = None


# ----------------------- helpers -----------------------
def run(cmd, cwd: str | Path | None = None, timeout=None):
    """Run a subprocess and return (returncode, stdout, stderr). timeout -> (124,..)."""
    try:
        p = subprocess.run(
            cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    return p.returncode, p.stdout, p.stderr


def mutation_score(task_dir: str | Path):
    """Run mutmut if available; return (killed, total, score) or (None, None, None)."""
    if shutil.which("mutmut") is None:
        return None, None, None

    # clean any previous cache (best-effort)
    try:
        cache = Path(task_dir) / ".mutmut-cache"
        if cache.exists():
            cache.unlink()
    except Exception:
        pass

    # run mutmut via current Python (so it uses the venv)
    run(
        [
            sys.executable,
            "-m",
            "mutmut",
            "run",
            "--paths-to-mutate",
            "src",
            "--tests-dir",
            "tests",
            "--no-progress",
        ],
        cwd=task_dir,
        timeout=float(os.getenv("MUTMUT_TIMEOUT_S", "900")),
    )

    code, out, _ = run([sys.executable, "-m", "mutmut", "results"], cwd=task_dir)
    if code != 0:
        return None, None, None

    survived = killed = timeout = suspicious = 0
    for line in out.splitlines():
        m = re.search(r"Survived\s*\((\d+)\)", line)
        survived = int(m.group(1)) if m else survived
        m = re.search(r"Killed\s*\((\d+)\)", line)
        killed = int(m.group(1)) if m else killed
        m = re.search(r"Timeout\s*\((\d+)\)", line)
        timeout = int(m.group(1)) if m else timeout
        m = re.search(r"Suspicious\s*\((\d+)\)", line)
        suspicious = int(m.group(1)) if m else suspicious

    total = survived + killed + timeout + suspicious
    if total == 0:
        return 0, 0, None
    score = killed / total
    return killed, total, round(score, 3)


def junit_results(junit_path: Path):
    total = passed = failed = errors = 0
    try:
        root = ET.parse(junit_path).getroot()
        for ts in root.findall(".//testsuite"):
            total += int(ts.attrib.get("tests", 0))
            failed += int(ts.attrib.get("failures", 0))
            errors += int(ts.attrib.get("errors", 0))
        passed = max(0, total - failed - errors)
    except Exception:
        pass
    return dict(total=total, passed=passed, failed=failed, errors=errors)


# NOTE: lint_score, complexity_score and security_score below are LEGACY
# normalized indicators. They are NOT used in the published results, which
# report flake8 violations per 100 logical lines, raw cyclomatic complexity,
# and bandit/semgrep findings by severity (see scripts/remeasure_quality.py).
# They are retained so earlier runs remain reproducible.

def radon_complexity_score(py_files: list[str]):
    if not cc_visit or not py_files:
        return None, None
    vals = []
    for f in py_files:
        try:
            blocks = cc_visit(Path(f).read_text(encoding="utf-8"))
            vals += [b.complexity for b in blocks]
        except Exception:
            pass
    if not vals:
        return None, None
    avg = mean(vals)
    # Normalize: <=5 -> 1.0 ; >=15 -> 0.0
    score = 1.0 if avg <= 5 else (0.0 if avg >= 15 else 1 - (avg - 5) / 10)
    return round(avg, 3), round(score, 3)


def flake8_issues(path: str | Path):
    if not flake8_api:
        return None, None
    sg = flake8_api.get_style_guide(max_line_length=120)
    report = sg.check_files([str(path)])
    n = getattr(report, "total_errors", 0)
    score = max(0.0, 1 - min(n, 20) / 20)
    return n, round(score, 3)


def bandit_issues(path: str | Path):
    code, out, _ = run(["bandit", "-r", ".", "-f", "json", "-q"], cwd=path)
    try:
        data = json.loads(out)
        n = len(data.get("results", []))
    except Exception:
        n = None
    if n is None:
        return None, None
    score = max(0.0, 1 - min(n, 20) / 20)
    return n, round(score, 3)


def semgrep_issues(path: str | Path):
    """Optional second security signal (Semgrep). Descriptive only, NOT in the
    composite. Returns (count, None) or (None, None) if semgrep is unavailable.
    Install: pip install semgrep."""
    if shutil.which("semgrep") is None:
        return None, None
    code, out, _ = run(
        ["semgrep", "--quiet", "--json", "--config", "p/python", "."], cwd=path
    )
    try:
        n = len(json.loads(out).get("results", []))
    except Exception:
        n = None
    return n, None


def pip_audit(req_path: str | Path):
    req = Path(req_path)
    if not req.exists():
        return None, None
    code, out, _ = run(
        [sys.executable, "-m", "pip_audit", "-r", str(req), "-f", "json"]
    )
    try:
        data = json.loads(out)
        n = sum(len(p.get("vulns", [])) for p in data)
    except Exception:
        n = None
    if n is None:
        return None, None
    score = max(0.0, 1 - min(n, 10) / 10)
    return n, round(score, 3)


def discover_tasks(root: str | Path):
    tasks: list[dict] = []
    for p in sorted(Path(root).glob("*")):
        if not p.is_dir():
            continue
        meta = {"id": p.name, "path": str(p)}
        mf = p / "task.yaml"
        if mf.exists():
            try:
                import yaml

                y = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
                if isinstance(y, dict):
                    meta.update(y)
            except Exception:
                pass
        tasks.append(meta)
    return tasks


def evaluate_task(task: dict):
    tdir = Path(task["path"]).resolve()
    src = tdir / "src"
    # Grade on the HIDDEN test suite (models only see tests_public). Revision T1.3.
    tests = tdir / "tests_hidden"
    py_files = [str(p) for p in src.rglob("*.py")]

    res: dict[str, object] = {
        "id": task["id"],
        "title": task.get("title", task["id"]),
    }

    # 1) Correctness via pytest (use venv python)
    junit = tdir / "reports" / "junit.xml"
    junit.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--disable-warnings",
            f"--junitxml={junit}",
            str(tests),
        ],
        cwd=str(tdir),
        timeout=float(os.getenv("PYTEST_TIMEOUT_S", "60")),
    )
    jt = junit_results(junit)
    res["tests"] = jt
    res["correctness"] = round(jt["passed"] / jt["total"], 3) if jt["total"] else 0.0

    # 2) Complexity
    avg_cc, cc_score = radon_complexity_score(py_files)
    res["complexity_avg"] = avg_cc
    res["complexity_score"] = cc_score

    # 3) Lint
    lint_cnt, lint_score = flake8_issues(src)
    res["lint_issues"] = lint_cnt
    res["lint_score"] = lint_score

    # 4) Security
    sec_cnt, sec_score = bandit_issues(src)
    res["security_issues"] = sec_cnt
    res["security_score"] = sec_score
    # Second, descriptive security signal (Semgrep), not folded into the composite.
    semgrep_cnt, _ = semgrep_issues(src)
    res["security_semgrep_issues"] = semgrep_cnt

    # 5) Dependencies
    dep_cnt, dep_score = pip_audit(tdir / "requirements.txt")
    res["dep_vulns"] = dep_cnt
    res["dep_score"] = dep_score

    # 6) Mutation testing (robustness) -- only when the solution has executable,
    #    passing code (correctness > 0). Mutation adequacy is undefined for a
    #    zero-correctness (failed/hanging) solution; such tasks are excluded, as
    #    documented in the paper's threats.
    # Mutation is now a BENCHMARK-validation measure computed separately on the
    # reference solutions (scripts/validate_test_suites.py), NOT a per-solution
    # code-quality axis. Skip it here for speed and to keep it out of the
    # composite.
    killed, total, mut_score = (None, None, None)
    res["mut_killed"] = killed
    res["mut_total"] = total
    res["mutation_score"] = mut_score

    # Note: per-task aggregate will be computed later using metrics weights
    return res


# ----------------------- output writers -----------------------
def write_scorecard(results: dict, md: str = "scorecard.md"):
    def fmt(x):
        return "—" if x is None else f"{x:.2f}"

    lines = [
        "# CodeAssay Scorecard",
        "",
        f"**Overall mean score:** {results['aggregate']['mean_score']:.3f}",
        "",
        "| Task | Correct | Complx | Lint | Sec | Deps | Mutation | Aggregate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for t in results["tasks"]:
        lines.append(
            f"| {t['id']} | {fmt(t.get('correctness', 0))} | "
            f"{fmt(t.get('complexity_score'))} | {fmt(t.get('lint_score'))} | "
            f"{fmt(t.get('security_score'))} | {fmt(t.get('dep_score'))} | "
            f"{fmt(t.get('mutation_score'))} | {fmt(t.get('aggregate_score', 0))} |"
        )

    Path(md).write_text("\n".join(lines), encoding="utf-8")


def write_csv(results: dict, csv_path: str = "results.csv"):
    """Export per-task metrics to a flat CSV for analysis/papers."""
    fields = [
        "id",
        "title",
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

    def fmt(v):
        if v is None:
            return ""
        if isinstance(v, float):
            return f"{v:.3f}"
        return v

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in results["tasks"]:
            row = {
                "id": t["id"],
                "title": t.get("title", ""),
                "tests_total": t.get("tests", {}).get("total"),
                "tests_passed": t.get("tests", {}).get("passed"),
                "tests_failed": t.get("tests", {}).get("failed"),
                "tests_errors": t.get("tests", {}).get("errors"),
                "correctness": t.get("correctness"),
                "complexity_avg": t.get("complexity_avg"),
                "complexity_score": t.get("complexity_score"),
                "lint_issues": t.get("lint_issues"),
                "lint_score": t.get("lint_score"),
                "security_issues": t.get("security_issues"),
                "security_score": t.get("security_score"),
                "dep_vulns": t.get("dep_vulns"),
                "dep_score": t.get("dep_score"),
                "mutation_killed": t.get("mut_killed"),
                "mutation_total": t.get("mut_total"),
                "mutation_score": t.get("mutation_score"),
                "aggregate_score": t.get("aggregate_score"),
            }
            w.writerow({k: fmt(v) for k, v in row.items()})

        # Optional: a final aggregate row
        w.writerow(
            {
                "id": "__aggregate__",
                "title": f"mean over {results['aggregate'].get('num_tasks', '')} tasks",
                "aggregate_score": f"{results['aggregate']['mean_score']:.3f}",
            }
        )


# ----------------------- metrics config -----------------------
def load_metrics_config(path: str | None):
    default = {
        "id": "VibeBench-default",
        "missing_metric": "skip",
        "weights": {"correctness": 1.0},
    }
    if not path:
        return default, None
    p = Path(path)
    if not p.exists():
        return default, None
    txt = p.read_text(encoding="utf-8")
    sha = hashlib.sha256(txt.encode("utf-8")).hexdigest()[:12]
    cfg = json.loads(txt)
    return cfg, {"path": str(p), "sha256_12": sha}


def weighted_aggregate(
    row: dict, weights: dict[str, float], missing: str = "skip"
) -> float:
    # Strict correctness gate: quality axes are credited only for solutions that
    # pass ALL hidden tests (correctness == 1.0).
    correctness = row.get("correctness")
    if correctness is not None and correctness != "" and float(correctness) < 1.0:
        return 0.0
    num = 0.0
    den = 0.0
    for k, w in weights.items():
        v = row.get(k)
        if v is None or v == "":
            if missing == "zero":
                num += 0.0
                den += w
            elif missing == "skip":
                continue
        else:
            num += float(v) * w
            den += w
    return 0.0 if den == 0 else num / den


# ----------------------- entry point -----------------------
def main():
    ap = argparse.ArgumentParser(description="CodeAssay Runner")
    ap.add_argument("--tasks", default="tasks/python", help="Path to tasks root")
    ap.add_argument("--out", default="results.json", help="Output JSON path")
    ap.add_argument(
        "--csv", dest="csv_out", default="results.csv", help="CSV export path"
    )
    ap.add_argument(
        "--metrics",
        default="configs/metrics.v2.json",
        help="Path to a LEGACY composite-weights file. The composite is not used in the published results; correctness and each quality indicator are reported separately.",
    )
    ap.add_argument("--limit", type=int, default=0,
                    help="Grade only the first N tasks (0=all); for smoke tests.")
    args = ap.parse_args()

    # discover, evaluate
    tasks = discover_tasks(args.tasks)
    if args.limit:
        tasks = tasks[: args.limit]
    results = [evaluate_task(t) for t in tasks]

    # load metrics weights and compute per-task aggregate
    metrics_cfg, metrics_meta = load_metrics_config(args.metrics)
    weights = metrics_cfg.get("weights", {})
    missing = metrics_cfg.get("missing_metric", "skip")

    for r in results:
        r["aggregate_score"] = round(weighted_aggregate(r, weights, missing), 3)

    mean_score = round(
        sum(r["aggregate_score"] for r in results) / max(1, len(results)), 3
    )
    out = {
        "tasks": results,
        "aggregate": {
            "mean_score": mean_score,
            "num_tasks": len(results),
            "metrics_id": metrics_cfg.get("id", "unknown"),
            "metrics_weights": weights,
            "metrics_missing_policy": missing,
            "metrics_config": metrics_meta or {},
        },
    }

    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    write_scorecard(out)
    write_csv(out, args.csv_out)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
