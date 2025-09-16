#!/usr/bin/env python3
import argparse, json, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
from statistics import mean

#Optional imports

try:
    from radon.complexity import cc_visit
except Exception:
    cc_visit = None
try:
    from flake8.api import legacy as flake8_api
except Exception:
    flake8_api = None

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
    if not cc_visit or not py_files: return None, None
    vals = []
    for f in py_files:
        try:
            blocks = cc_visit(Path(f).read_text(encoding="utf-8"))
            vals += [b.complexity for b in blocks]
        except Exception:
            pass
    if not vals: return None, None
    avg = mean(vals)
    # Normalize: <=5 -> 1.0 ; >=15 -> 0.0
    score = 1.0 if avg <= 5 else (0.0 if avg >= 15 else 1 - (avg - 5)/10)
    return round(avg,3), round(score,3)

def flake8_issues(path):
    if not flake8_api: return None, None
    sg = flake8_api.get_style_guide(max_line_length=120)
    report = sg.check_files([path])
    n = getattr(report, "total_errors", 0)
    score = max(0.0, 1 - min(n, 20)/20)
    return n, round(score,3)

def bandit_issues(path):
    code, out, _ = run(["bandit", "-r", ".", "-f", "json", "-q"], cwd=path)
    try:
        data = json.loads(out); n = len(data.get("results", []))
    except Exception:
        n = None
    if n is None: return None, None
    score = max(0.0, 1 - min(n, 20)/20)
    return n, round(score,3)

def pip_audit(req_path):
    req = Path(req_path)
    if not req.exists(): return None, None
    code, out, _ = run(["pip-audit", "-r", str(req), "-f", "json"])
    try:
        data = json.loads(out); n = sum(len(p.get("vulns", [])) for p in data)
    except Exception:
        n = None
    if n is None: return None, None
    score = max(0.0, 1 - min(n, 10)/10)
    return n, round(score,3)

def discover_tasks(root):
    tasks=[]
    for p in sorted(Path(root).glob("*")):
        if p.is_dir():
            meta={"id":p.name,"path":str(p)}
            mf = p/"task.yaml"
        if mf.exists():
            try:
                import yaml
                meta.update(yaml.safe_load(mf.read_text(encoding="utf-8")) or {})
            except Exception:
                pass
        tasks.append(meta)
    return tasks

def evaluate_task(task):
    tdir = Path(task["path"]); src=tdir/"src"; tests=tdir/"tests"
    py_files = [str(p) for p in src.rglob("*.py")]
    res={"id":task, "title":task.get("title", task["id"])}
    # Correctness   
    junit = tdir/"reports"/"junit.xml"; junit.parent.mkdir(exist_ok=True)
    run(["pytest","-q","--disable-warnings","--maxfail=1",f"--junitxml={junit}",str(tests)], cwd=str(tdir))
    jt = junit_results(junit)
    res["tests"]=jt
    res["correctness"]=round(jt["passed"]/jt["total"],3) if jt["total"] else 0.0

    # Complexity
    avg_cc, cc_score = radon_complexity_score(py_files)
    res["complexity_avg"]=avg_cc; res["complexity_score"]=cc_score

    # Lint
    lint_cnt, lint_score = flake8_issues(str(src))
    res["lint_issues"]=lint_cnt; res["lint_score"]=lint_score

    # Security
    sec_cnt, sec_score = bandit_issues(str(src))
    res["security_issues"]=sec_cnt; res["security_score"]=sec_score

    # Dependencies
    dep_cnt, dep_score = pip_audit(str(tdir/"requirements.txt"))
    res["dep_vulns"]=dep_cnt; res["dep_score"]=dep_score

    subs=[res["correctness"], cc_score, lint_score, sec_score, dep_score]
    subs=[x for x in subs if isinstance(x,float)]
    res["aggregate_score"]=round(sum(subs)/len(subs),3) if subs else 0.0
    return res

def write_scorecard(results, md="scorecard.md"):
    def fmt(x):
        return "—" if x is None else f"{x:.2f}"

    lines = [
        "# VibeBench-Mini Scorecard",
        "",
        f"**Overall mean score:** {results['aggregate']['mean_score']:.3f}",
        "",
        "| Task | Correct | Complx | Lint | Sec | Deps | Aggregate |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for t in results["tasks"]:
        lines.append(
            f"| {t['id']} | {fmt(t.get('correctness', 0))} | {fmt(t.get('complexity_score'))} | "
            f"{fmt(t.get('lint_score'))} | {fmt(t.get('security_score'))} | "
            f"{fmt(t.get('dep_score'))} | {fmt(t.get('aggregate_score', 0))} |"
        )

    Path(md).write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="VibeBench-Mini Runner")
    ap.add_argument("--tasks", default="tasks/python", help="Path to tasks root")
    ap.add_argument("--out", default="results.json", help="Output JSON path")
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
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

