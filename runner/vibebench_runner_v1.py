#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import re
import shutil
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


def mutation_score(task_dir):
    """Run mutmut if available; return (killed, total, score) or (None, None, None)."""
    if shutil.which("mutmut") is None:
        return None, None, None

    # clean any previous cache
    try:
        cache = Path(task_dir) / ".mutmut-cache"
        if cache.exists():
            cache.unlink()
    except Exception:
        pass

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
    )

    code, out, err = run([sys.executable, "-m", "mutmut", "results"], cwd=task_dir)
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


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


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


def radon_complexity_score(py_files):
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


def flake8_issues(path):
    if not flake8_api:
        return None, None
    sg = flake8_api.get_style_guide(max_line_length=120)
    report = sg.check_files([path])
    n = getattr(report, "total_errors", 0)
    score = max(0.0, 1 - min(n, 20) / 20)
    return n, round(score, 3)


def bandit_issues(path):
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


def pip_audit(req_path):
    req = Path(req_path)
    if not req.exists():
        return None, None
    code, out, _ = run(["pip-audit", "-r", str(req), "-f", "json"])
    try:
        data = json.loads(out)
        n = sum(len(p.get("vulns", [])) for p in data)
    except Exception:
        n = None
    if n is None:
        return None, None
    score = max(0.0, 1 - min(n, 10) / 10)
    return n, round(score, 3)


def discover_tasks(root):
    tasks = []
    for p in sorted(Path(root).glob("*")):
        if p.is_dir():
            meta = {"id": p.name, "path": str(p)}
            mf = p / "task.yaml"
        if mf.exists():
            try:
                import yaml

                meta.update(yaml.safe_load(mf.read_text(encoding="utf-8")) or {})
            except Exception:
                pass
        tasks.append(meta)
    return tasks


def evaluate_task(task):
    tdir = Path(task["path"])
    src = tdir / "src"
    tests = tdir / "tests"
    py_files = [str(p) for p in src.rglob("*.py")]
    res = {"id": task, "title": task.get("title", task["id"])}
    # Correctness
    junit = tdir / "reports" / "junit.xml"
    junit.parent.mkdir(exist_ok=True)
    run(
        [
            "pytest",
            "-q",
            "--disable-warnings",
            "--maxfail=1",
            f"--junitxml={junit}",
            str(tests),
        ],
        cwd=str(tdir),
    )
    jt = junit_results(junit)
    res["tests"] = jt
    res["correctness"] = round(jt["passed"] / jt["total"], 3) if jt["total"] else 0.0

    # Complexity
    avg_cc, cc_score = radon_complexity_score(py_files)
    res["complexity_avg"] = avg_cc
    res["complexity_score"] = cc_score

    # Lint
    lint_cnt, lint_score = flake8_issues(str(src))
    res["lint_issues"] = lint_cnt
    res["lint_score"] = lint_score

    # Security
    sec_cnt, sec_score = bandit_issues(str(src))
    res["security_issues"] = sec_cnt
    res["security_score"] = sec_score

    # Dependencies
    dep_cnt, dep_score = pip_audit(str(tdir / "requirements.txt"))
    res["dep_vulns"] = dep_cnt
    res["dep_score"] = dep_score

    # 6) Mutation testing (robustness)
    killed, total, mut_score = mutation_score(str(tdir))
    res["mut_killed"] = killed
    res["mut_total"] = total
    res["mutation_score"] = mut_score

    subscores = [res["correctness"], cc_score, lint_score, sec_score, dep_score]
    if isinstance(mut_score, float):
        subscores.append(mut_score)

    subs = [res["correctness"], cc_score, lint_score, sec_score, dep_score]
    subs = [x for x in subs if isinstance(x, float)]
    res["aggregate_score"] = round(sum(subs) / len(subs), 3) if subs else 0.0
    return res


def write_scorecard(results, md="scorecard.md"):
    def fmt(x):
        return "—" if x is None else f"{x:.2f}"

    # lines = [
    #     "# VibeBench-Mini Scorecard",
    #     "",
    #     f"**Overall mean score:** {results['aggregate']['mean_score']:.3f}",
    #     "",
    #     "| Task | Correct | Complx | Lint | Sec | Deps | Aggregate |",
    #     "|---|---:|---:|---:|---:|---:|---:|",
    # ]
    lines = [
        "# VibeBench-Mini Scorecard",
        "",
        f"**Overall mean score:** {results['aggregate']['mean_score']:.3f}",
        "",
        "| Task | Correct | Complx | Lint | Sec | Deps | Mutation | Aggregate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for t in results["tasks"]:
        # lines.append(
        #     f"| {t['id']} | {fmt(t.get('correctness', 0))} | {fmt(t.get('complexity_score'))} | "
        #     f"{fmt(t.get('lint_score'))} | {fmt(t.get('security_score'))} | "
        #     f"{fmt(t.get('dep_score'))} | {fmt(t.get('aggregate_score', 0))} |"
        # )
        lines.append(
            f"| {t['id']} | {fmt(t.get('correctness', 0))} | "
            f"{fmt(t.get('complexity_score'))} | {fmt(t.get('lint_score'))} | "
            f"{fmt(t.get('security_score'))} | {fmt(t.get('dep_score'))} | "
            f"{fmt(t.get('mutation_score'))} | {fmt(t.get('aggregate_score', 0))} |"
        )

    Path(md).write_text("\n".join(lines), encoding="utf-8")


def write_csv(results, csv_path="results.csv"):
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


def main():
    ap = argparse.ArgumentParser(description="VibeBench-Mini Runner")
    ap.add_argument("--tasks", default="tasks/python", help="Path to tasks root")
    ap.add_argument("--out", default="results.json", help="Output JSON path")
    ap.add_argument(
        "--csv", dest="csv_out", default="results.csv", help="CSV export path"
    )
    # ap.add_argument("--metrics", default="configs/metrics.v1.json",
    #             help="Path to metrics.json (weights). Default: configs/metrics.v1.json")

    args = ap.parse_args()

    tasks = discover_tasks(args.tasks)
    results = [evaluate_task(t) for t in tasks]
    mean_score = round(
        sum(r["aggregate_score"] for r in results) / max(1, len(results)), 3
    )
    out = {
        "tasks": results,
        "aggregate": {"mean_score": mean_score, "num_tasks": len(results)},
    }

    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    write_scorecard(out)
    write_csv(out, args.csv_out)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
