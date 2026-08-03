#!/usr/bin/env python3.12
"""Re-measure every stored solution with the raw, unnormalized quality tools.

The published quality indicators were three
normalized scores:

  lint_score        = max(0, 1 - min(flake8_count, 20) / 20)
  security_score    = max(0, 1 - min(bandit_count, 20) / 20)
  complexity_score  = 1 if mean_cc <= 5 else (0 if mean_cc >= 15 else 1-(cc-5)/10)

All three are unsound as reported. The style score is a raw violation count that
ignores program length, so a longer program is penalised for being longer; it is
also censored at 20, which discards the tail. The security score collapses
Bandit findings of different severities into one number and censors it the same
way. The complexity score is a piecewise-linear rescaling whose knees at 5 and
15 have no justification in the literature we cite.

This script re-runs the same three tools on the same stored solutions and emits
the raw measurements, so that the analysis can report:

  style       flake8 violations per 100 logical lines (and per 100 source lines)
  complexity  raw mean cyclomatic complexity, plus raw maximum
  security    Bandit and Semgrep finding counts BY SEVERITY, descriptively

Tool invocations reproduce the runner's:
  flake8   max-line-length 120, repo .flake8 extend-ignore E203,W503
  bandit   bandit -r <dir> -f json -q
  radon    radon.complexity.cc_visit for CC, radon.raw.analyze for line counts
Semgrep findings are read from reports/semgrep_findings.csv, produced by
scripts/run_semgrep_scan.py (Semgrep skips dot-directories, so it stages the
solutions out of .agent_runs before scanning).

Output:
  reports/quality_remeasured.csv   one row per (configuration, prompt, task)

The stored per-task values in .agent_runs/<config>/results.csv are used as a
validation target: the flake8 and Bandit totals must match exactly and the mean
cyclomatic complexity to within rounding. The deltas are printed.

The corpus is selected with --runs-prefix. The default, an empty prefix, reads
.agent_runs/<slug>-<prompt> and writes reports/quality_remeasured.csv, which is
the original behaviour. A prefix such as "r2-" reads .agent_runs/r2-<slug>-<prompt>
and writes reports/r2_quality_remeasured.csv, with the Semgrep findings file and
the correctness source derived the same way. The r2 runs have no results.csv,
because their scoring runners were stopped; correctness for them is read from
the final_hidden_pass column of reports/<tag>_repair_audit.csv, and the
validation section reports the row count and the number of solutions that fail
ast.parse instead of the stored-value deltas.

Run:  python3.12 scripts/remeasure_quality.py
      python3.12 scripts/remeasure_quality.py --runs-prefix r2- --semgrep scan
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from radon.complexity import cc_visit
from radon.raw import analyze as raw_analyze

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / ".agent_runs"
REPORTS = ROOT / "reports"
TASKS = ROOT / "tasks" / "python"

FLAKE8 = ROOT / ".venv" / "bin" / "flake8"
BANDIT = ROOT / ".venv" / "bin" / "bandit"
SEMGREP = ROOT / ".venv" / "bin" / "semgrep"
SEMGREP_RULESETS = ["p/python", "p/security-audit"]

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

# Whitespace-only pycodestyle codes. These are cosmetic and a formatter removes
# all of them; they are broken out so the style indicator can be reported both
# with and without them.
WHITESPACE_CODES = ["W291", "W293", "W391", "E303"]

FLAKE8_ARGS = ["--max-line-length=120", "--extend-ignore=E203,W503"]


# --------------------------------------------------------------------------
# corpus selection
# --------------------------------------------------------------------------
def corpus_tag(runs_prefix: str) -> str:
    """"" for the original corpus, "r2" for --runs-prefix r2-."""
    return runs_prefix.strip("-")


def out_path(tag: str, stem: str) -> Path:
    """reports/<stem> for the original corpus, reports/<tag>_<stem> otherwise."""
    return REPORTS / (f"{tag}_{stem}" if tag else stem)


# --------------------------------------------------------------------------
# staging
# --------------------------------------------------------------------------
def stage_config(slug: str, prompt: str, root: Path, runs_prefix: str = "") -> tuple[Path, dict[str, str]]:
    """Copy one run's cached solutions to <root>/<slug>-<prompt>/<task>.py.

    Renaming to the bare task id keeps the file->task mapping trivial for every
    tool, and staging out of `.agent_runs` avoids the dot-directory exclusion
    that both flake8 (repo .flake8 exclude list) and Semgrep apply.
    """
    cache = RUNS / f"{runs_prefix}{slug}-{prompt}" / "cache"
    if not cache.is_dir():
        raise SystemExit(f"missing cache directory: {cache}")
    dest = root / f"{slug}-{prompt}"
    dest.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, str] = {}
    for f in sorted(cache.glob("*.py")):
        task = f.name.split("__")[0]
        shutil.copy(f, dest / f"{task}.py")
        mapping[f"{task}.py"] = task
    return dest, mapping


def stage_reference(root: Path) -> tuple[Path, dict[str, str]]:
    """Copy the 185 reference solutions to <root>/reference/<task>.py."""
    dest = root / "reference"
    dest.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, str] = {}
    for task in sorted(TASKS.glob("task*")):
        src = task / "src" / "solution.py"
        if src.is_file():
            shutil.copy(src, dest / f"{task.name}.py")
            mapping[f"{task.name}.py"] = task.name
    return dest, mapping


# --------------------------------------------------------------------------
# measurement
# --------------------------------------------------------------------------
def measure_flake8(directory: Path, mapping: dict[str, str]) -> dict[str, Counter]:
    """flake8 violation codes per task. One process per configuration."""
    cmd = [str(FLAKE8), *FLAKE8_ARGS, "--format=%(path)s\t%(code)s", str(directory)]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    out: dict[str, Counter] = {t: Counter() for t in mapping.values()}
    for line in proc.stdout.splitlines():
        if "\t" not in line:
            continue
        path, code = line.rsplit("\t", 1)
        task = mapping.get(Path(path).name)
        if task is None:
            continue
        out[task][code.strip()] += 1
    return out


def measure_bandit(directory: Path, mapping: dict[str, str]) -> dict[str, dict]:
    """Bandit findings per task, split by severity, confidence and test id."""
    proc = subprocess.run(
        [str(BANDIT), "-r", str(directory), "-f", "json", "-q"],
        capture_output=True,
        text=True,
    )
    empty = {
        "sev": Counter(),
        "conf": Counter(),
        "tests": Counter(),
        "total": 0,
        "loc": None,
    }
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"  ! bandit produced no JSON for {directory.name}", file=sys.stderr)
        return {t: dict(empty, sev=Counter(), conf=Counter(), tests=Counter()) for t in mapping.values()}

    out: dict[str, dict] = {
        t: {"sev": Counter(), "conf": Counter(), "tests": Counter(), "total": 0, "loc": None}
        for t in mapping.values()
    }
    for r in data.get("results", []):
        task = mapping.get(Path(r.get("filename", "")).name)
        if task is None:
            continue
        rec = out[task]
        rec["total"] += 1
        rec["sev"][r.get("issue_severity", "UNDEFINED")] += 1
        rec["conf"][r.get("issue_confidence", "UNDEFINED")] += 1
        rec["tests"][r.get("test_id", "")] += 1
    for fname, m in data.get("metrics", {}).items():
        if fname == "_totals":
            continue
        task = mapping.get(Path(fname).name)
        if task is None:
            continue
        out[task]["loc"] = m.get("loc")
        # cross-check: the metrics block counts the same findings by severity
        for key, sev in (
            ("SEVERITY.HIGH", "HIGH"),
            ("SEVERITY.MEDIUM", "MEDIUM"),
            ("SEVERITY.LOW", "LOW"),
            ("SEVERITY.UNDEFINED", "UNDEFINED"),
        ):
            n = int(m.get(key, 0) or 0)
            if n != out[task]["sev"].get(sev, 0):
                print(
                    f"  ! bandit severity mismatch {directory.name}/{task} {sev}: "
                    f"metrics {n} vs results {out[task]['sev'].get(sev, 0)}",
                    file=sys.stderr,
                )
    return out


def measure_radon(directory: Path, mapping: dict[str, str]) -> dict[str, dict]:
    """Raw line counts and raw cyclomatic complexity per task."""
    out: dict[str, dict] = {}
    for fname, task in mapping.items():
        src = (directory / fname).read_text(encoding="utf-8", errors="replace")
        rec = {
            "loc": None, "lloc": None, "sloc": None, "comments": None,
            "blank": None, "raw_ok": 0,
            "cc_mean": None, "cc_max": None, "cc_blocks": 0, "cc_ok": 0,
        }
        try:
            r = raw_analyze(src)
            rec.update(loc=r.loc, lloc=r.lloc, sloc=r.sloc, comments=r.comments,
                       blank=r.blank, raw_ok=1)
        except Exception:
            pass
        try:
            blocks = cc_visit(src)
            vals = [b.complexity for b in blocks]
            rec["cc_ok"] = 1
            rec["cc_blocks"] = len(vals)
            if vals:
                rec["cc_mean"] = sum(vals) / len(vals)
                rec["cc_max"] = max(vals)
        except Exception:
            pass
        out[task] = rec
    return out


def load_semgrep(path: Path) -> dict[tuple[str, str, str], dict]:
    """Semgrep findings keyed by (config display name, prompt, task)."""
    out: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {"sev": Counter(), "rulesets": Counter(), "rules": Counter()}
    )
    if not path.exists():
        print(f"  ! {path} missing; semgrep columns will be 0")
        return out
    with path.open() as fh:
        for row in csv.DictReader(fh):
            task = Path(row["file"]).name.split("__")[0].removesuffix(".py")
            key = (row["configuration"], row["prompt"], task)
            out[key]["sev"][row["severity"]] += 1
            out[key]["rulesets"][row["ruleset"]] += 1
            out[key]["rules"][row["check_id"]] += 1
    return out


def semgrep_bin() -> str:
    if SEMGREP.exists():
        return str(SEMGREP)
    found = shutil.which("semgrep")
    if not found:
        raise SystemExit("semgrep not found; pip install semgrep")
    return found


def semgrep_scan(directory: Path, ruleset: str) -> tuple[list[dict], int]:
    """Run one ruleset over one staged directory. Returns (findings, n_scanned).

    The staging root is a temporary directory outside the repository. Semgrep
    skips dot-directories and honours .gitignore, so staging inside the repo
    silently scans zero files; the caller asserts the scanned count.
    """
    proc = subprocess.run(
        [semgrep_bin(), "--quiet", "--json", "--config", ruleset, str(directory)],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise SystemExit(
            f"semgrep produced no JSON for {directory.name}/{ruleset}: "
            f"{proc.stderr[:400]}"
        )
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


def run_semgrep(staged: list[tuple[str, str, Path]], out_csv: Path) -> None:
    """Scan every staged configuration with every ruleset and write the CSV.

    Fails loudly if any scan reports zero files or a count other than the number
    of staged files, which is the failure mode the earlier in-repo staging hit.
    """
    rows: list[dict] = []
    for name, prompt, directory in staged:
        n_staged = len(list(directory.glob("*.py")))
        for ruleset in SEMGREP_RULESETS:
            findings, scanned = semgrep_scan(directory, ruleset)
            print(
                f"  semgrep {name} [{prompt}] {ruleset}: "
                f"{scanned}/{n_staged} files scanned, {len(findings)} findings",
                flush=True,
            )
            if scanned == 0 or scanned != n_staged:
                raise SystemExit(
                    f"semgrep scanned {scanned} of {n_staged} staged files in "
                    f"{directory} with {ruleset}; refusing to report a partial scan"
                )
            for f in findings:
                rows.append(
                    {"configuration": name, "prompt": prompt, "ruleset": ruleset, **f}
                )
    fields = ["configuration", "prompt", "ruleset", "file", "check_id", "severity", "message"]
    with out_csv.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=fields)
        wr.writeheader()
        wr.writerows(rows)
    print(f"wrote {out_csv}  ({len(rows)} findings)")


# --------------------------------------------------------------------------
# stored values, for validation
# --------------------------------------------------------------------------
def load_stored(slug: str, prompt: str, runs_prefix: str = "") -> dict[str, dict]:
    path = RUNS / f"{runs_prefix}{slug}-{prompt}" / "results.csv"
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    with path.open() as fh:
        for row in csv.DictReader(fh):
            if row["id"] == "__aggregate__":
                continue
            out[row["id"]] = row
    return out


def load_audit_correct(path: Path) -> dict[tuple[str, str, str], int]:
    """{(slug, prompt, task): 0/1} from the repair audit's final_hidden_pass.

    This is the correctness source for a corpus whose scoring runners were not
    run, so no results.csv exists. The audit's `run` column is
    <prefix><slug>-<prompt>, which is what the slug and prompt are recovered from.
    """
    out: dict[tuple[str, str, str], int] = {}
    if not path.exists():
        raise SystemExit(f"missing correctness source: {path}")
    with path.open() as fh:
        for row in csv.DictReader(fh):
            run = row["run"]
            body = run.split("-", 1)[1] if run.startswith("r2-") else run
            slug, _, prompt = body.rpartition("-")
            out[(slug, prompt, row["task"])] = 1 if row["final_hidden_pass"] == "True" else 0
    return out


def parses(path: Path) -> bool:
    try:
        ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        return True
    except SyntaxError:
        return False


def as_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def as_int(x):
    v = as_float(x)
    return None if v is None else int(v)


def counter_str(c: Counter) -> str:
    return ";".join(f"{k}:{v}" for k, v in sorted(c.items()) if v)


# --------------------------------------------------------------------------
FIELDS = [
    "config", "config_name", "prompt", "task", "correct",
    # flake8
    "flake8_total", "flake8_ws", "flake8_nonws",
    *[f"flake8_{c}" for c in WHITESPACE_CODES],
    "flake8_codes",
    # size
    "raw_loc", "lloc", "sloc", "comments", "blank", "radon_raw_ok", "bandit_loc",
    # complexity
    "cc_mean", "cc_max", "cc_blocks", "radon_cc_ok",
    # style, normalized
    "style_per100_lloc", "style_per100_sloc",
    "style_nonws_per100_lloc",
    # bandit
    "bandit_total", "bandit_high", "bandit_medium", "bandit_low", "bandit_undef",
    "bandit_conf_high", "bandit_conf_medium", "bandit_conf_low",
    "bandit_tests",
    # semgrep
    "semgrep_total", "semgrep_error", "semgrep_warning", "semgrep_info",
    "semgrep_rules",
    # stored values for audit
    "stored_lint_issues", "stored_security_issues", "stored_complexity_avg",
    "stored_lint_score", "stored_security_score", "stored_complexity_score",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep-stage", action="store_true",
                    help="keep the staging directory for inspection")
    ap.add_argument("--runs-prefix", default="",
                    help="prefix of the .agent_runs configuration directories; "
                         "'' is the original corpus, 'r2-' the regenerated one")
    ap.add_argument("--semgrep", choices=["read", "scan", "skip"], default="read",
                    help="read an existing findings CSV (default), run Semgrep "
                         "over the staged solutions and write it, or skip")
    args = ap.parse_args()

    tag = corpus_tag(args.runs_prefix)
    out = out_path(tag, "quality_remeasured.csv")
    semgrep_csv = out_path(tag, "semgrep_findings.csv")
    audit_csv = out_path(tag, "repair_audit.csv")

    REPORTS.mkdir(exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix="codeassay_remeasure_"))
    print(f"corpus prefix {args.runs_prefix!r}; staging in {stage_root}")

    rows: list[dict] = []
    deltas = {"flake8": [], "bandit": [], "cc": []}
    ast_fail: list[str] = []
    audit_correct: dict[tuple[str, str, str], int] = {}

    try:
        # stage everything first, so Semgrep can scan the same trees flake8,
        # Bandit and radon see
        staged: list[tuple[str, str, str, Path, dict[str, str]]] = []
        for slug, name in MODELS:
            for prompt in PROMPTS:
                directory, mapping = stage_config(slug, prompt, stage_root,
                                                  args.runs_prefix)
                staged.append((slug, name, prompt, directory, mapping))
                for fname in mapping:
                    if not parses(directory / fname):
                        ast_fail.append(f"{slug}-{prompt}/{fname}")
        ref_dir, ref_map = stage_reference(stage_root)

        if args.semgrep == "scan":
            run_semgrep(
                [(n, p, d) for _, n, p, d, _ in staged]
                + [("CodeAssay reference", "n/a", ref_dir)],
                semgrep_csv,
            )
        semgrep = {} if args.semgrep == "skip" else load_semgrep(semgrep_csv)

        for slug, name, prompt, directory, mapping in staged:
                cfg = f"{slug}-{prompt}"
                print(f"measuring {cfg} ({len(mapping)} files) ...", flush=True)
                f8 = measure_flake8(directory, mapping)
                bd = measure_bandit(directory, mapping)
                rd = measure_radon(directory, mapping)
                stored = load_stored(slug, prompt, args.runs_prefix)
                if not stored:
                    if not audit_correct:
                        audit_correct = load_audit_correct(audit_csv)

                for task in sorted(mapping.values()):
                    codes = f8[task]
                    ws = sum(codes.get(c, 0) for c in WHITESPACE_CODES)
                    tot = sum(codes.values())
                    b = bd[task]
                    r = rd[task]
                    sg = semgrep.get((name, prompt, task))
                    st = stored.get(task, {})

                    s_lint = as_int(st.get("lint_issues"))
                    s_sec = as_int(st.get("security_issues"))
                    s_cc = as_float(st.get("complexity_avg"))
                    if s_lint is not None:
                        deltas["flake8"].append(abs(tot - s_lint))
                    if s_sec is not None:
                        deltas["bandit"].append(abs(b["total"] - s_sec))
                    if s_cc is not None and r["cc_mean"] is not None:
                        deltas["cc"].append(abs(round(r["cc_mean"], 3) - s_cc))

                    lloc = r["lloc"]
                    sloc = r["sloc"]
                    rows.append(
                        {
                            "config": cfg,
                            "config_name": name,
                            "prompt": prompt,
                            "task": task,
                            "correct": (
                                1 if (as_float(st.get("correctness")) or 0.0) >= 1.0 else 0
                            ) if stored else audit_correct.get((slug, prompt, task), 0),
                            "flake8_total": tot,
                            "flake8_ws": ws,
                            "flake8_nonws": tot - ws,
                            **{f"flake8_{c}": codes.get(c, 0) for c in WHITESPACE_CODES},
                            "flake8_codes": counter_str(codes),
                            "raw_loc": r["loc"],
                            "lloc": lloc,
                            "sloc": sloc,
                            "comments": r["comments"],
                            "blank": r["blank"],
                            "radon_raw_ok": r["raw_ok"],
                            "bandit_loc": b["loc"],
                            "cc_mean": None if r["cc_mean"] is None else round(r["cc_mean"], 4),
                            "cc_max": r["cc_max"],
                            "cc_blocks": r["cc_blocks"],
                            "radon_cc_ok": r["cc_ok"],
                            "style_per100_lloc": None if not lloc else round(100 * tot / lloc, 4),
                            "style_per100_sloc": None if not sloc else round(100 * tot / sloc, 4),
                            "style_nonws_per100_lloc": None if not lloc else round(100 * (tot - ws) / lloc, 4),
                            "bandit_total": b["total"],
                            "bandit_high": b["sev"].get("HIGH", 0),
                            "bandit_medium": b["sev"].get("MEDIUM", 0),
                            "bandit_low": b["sev"].get("LOW", 0),
                            "bandit_undef": b["sev"].get("UNDEFINED", 0),
                            "bandit_conf_high": b["conf"].get("HIGH", 0),
                            "bandit_conf_medium": b["conf"].get("MEDIUM", 0),
                            "bandit_conf_low": b["conf"].get("LOW", 0),
                            "bandit_tests": counter_str(b["tests"]),
                            "semgrep_total": 0 if sg is None else sum(sg["sev"].values()),
                            "semgrep_error": 0 if sg is None else sg["sev"].get("ERROR", 0),
                            "semgrep_warning": 0 if sg is None else sg["sev"].get("WARNING", 0),
                            "semgrep_info": 0 if sg is None else sg["sev"].get("INFO", 0),
                            "semgrep_rules": "" if sg is None else counter_str(sg["rules"]),
                            "stored_lint_issues": s_lint,
                            "stored_security_issues": s_sec,
                            "stored_complexity_avg": s_cc,
                            "stored_lint_score": as_float(st.get("lint_score")),
                            "stored_security_score": as_float(st.get("security_score")),
                            "stored_complexity_score": as_float(st.get("complexity_score")),
                        }
                    )

        # reference solutions, as a human baseline row
        directory, mapping = ref_dir, ref_map
        print(f"measuring reference ({len(mapping)} files) ...", flush=True)
        f8 = measure_flake8(directory, mapping)
        bd = measure_bandit(directory, mapping)
        rd = measure_radon(directory, mapping)
        for task in sorted(mapping.values()):
            codes = f8[task]
            ws = sum(codes.get(c, 0) for c in WHITESPACE_CODES)
            tot = sum(codes.values())
            b = bd[task]
            r = rd[task]
            sg = semgrep.get(("CodeAssay reference", "n/a", task))
            lloc, sloc = r["lloc"], r["sloc"]
            rows.append(
                {
                    "config": "reference", "config_name": "CodeAssay reference",
                    "prompt": "ref", "task": task, "correct": 1,
                    "flake8_total": tot, "flake8_ws": ws, "flake8_nonws": tot - ws,
                    **{f"flake8_{c}": codes.get(c, 0) for c in WHITESPACE_CODES},
                    "flake8_codes": counter_str(codes),
                    "raw_loc": r["loc"], "lloc": lloc, "sloc": sloc,
                    "comments": r["comments"], "blank": r["blank"],
                    "radon_raw_ok": r["raw_ok"], "bandit_loc": b["loc"],
                    "cc_mean": None if r["cc_mean"] is None else round(r["cc_mean"], 4),
                    "cc_max": r["cc_max"], "cc_blocks": r["cc_blocks"],
                    "radon_cc_ok": r["cc_ok"],
                    "style_per100_lloc": None if not lloc else round(100 * tot / lloc, 4),
                    "style_per100_sloc": None if not sloc else round(100 * tot / sloc, 4),
                    "style_nonws_per100_lloc": None if not lloc else round(100 * (tot - ws) / lloc, 4),
                    "bandit_total": b["total"],
                    "bandit_high": b["sev"].get("HIGH", 0),
                    "bandit_medium": b["sev"].get("MEDIUM", 0),
                    "bandit_low": b["sev"].get("LOW", 0),
                    "bandit_undef": b["sev"].get("UNDEFINED", 0),
                    "bandit_conf_high": b["conf"].get("HIGH", 0),
                    "bandit_conf_medium": b["conf"].get("MEDIUM", 0),
                    "bandit_conf_low": b["conf"].get("LOW", 0),
                    "bandit_tests": counter_str(b["tests"]),
                    "semgrep_total": 0 if sg is None else sum(sg["sev"].values()),
                    "semgrep_error": 0 if sg is None else sg["sev"].get("ERROR", 0),
                    "semgrep_warning": 0 if sg is None else sg["sev"].get("WARNING", 0),
                    "semgrep_info": 0 if sg is None else sg["sev"].get("INFO", 0),
                    "semgrep_rules": "" if sg is None else counter_str(sg["rules"]),
                    "stored_lint_issues": None, "stored_security_issues": None,
                    "stored_complexity_avg": None, "stored_lint_score": None,
                    "stored_security_score": None, "stored_complexity_score": None,
                }
            )
    finally:
        if not args.keep_stage:
            shutil.rmtree(stage_root, ignore_errors=True)
        else:
            print(f"staging kept at {stage_root}")

    with out.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=FIELDS)
        wr.writeheader()
        wr.writerows(rows)

    # ---------------- validation ----------------
    gen = [r for r in rows if r["config"] != "reference"]
    expected = len(MODELS) * len(PROMPTS) * 185
    print()
    print(f"wrote {out}  ({len(rows)} rows, {len(gen)} generated + "
          f"{len(rows)-len(gen)} reference)")
    print()
    if deltas["flake8"]:
        print("Validation against the stored .agent_runs/*/results.csv values")
        print(f"  flake8 total  : n={len(deltas['flake8'])}  max |delta| = {max(deltas['flake8']):d}"
              f"  mismatches = {sum(1 for d in deltas['flake8'] if d)}")
        print(f"  bandit total  : n={len(deltas['bandit'])}  max |delta| = {max(deltas['bandit']):d}"
              f"  mismatches = {sum(1 for d in deltas['bandit'] if d)}")
        print(f"  radon mean CC : n={len(deltas['cc'])}  max |delta| = {max(deltas['cc']):.6f}"
              f"  above 5e-4 = {sum(1 for d in deltas['cc'] if d > 5e-4)}")
    else:
        print("No results.csv in this corpus, so there are no stored flake8 or")
        print("Bandit totals to validate against. Structural checks instead:")
        print(f"  generated rows: {len(gen)}  expected {expected}  "
              f"{'OK' if len(gen) == expected else 'MISMATCH'}")
        print(f"  correctness read from {audit_csv.name}: "
              f"{sum(r['correct'] for r in gen)} of {len(gen)} rows correct")
    print(f"  ast.parse failed on {len(ast_fail)} of {len(gen)} generated solutions"
          + (": " + ", ".join(ast_fail[:20]) if ast_fail else ""))
    n_raw_fail = sum(1 for r in gen if not r["radon_raw_ok"])
    n_cc_fail = sum(1 for r in gen if not r["radon_cc_ok"])
    print(f"  radon.raw failed on {n_raw_fail} generated files; "
          f"cc_visit failed on {n_cc_fail}")
    if deltas["flake8"] and (max(deltas["flake8"]) or max(deltas["bandit"])):
        raise SystemExit("VALIDATION FAILED: flake8/bandit totals do not reproduce")
    if not deltas["flake8"] and len(gen) != expected:
        raise SystemExit(
            f"VALIDATION FAILED: {len(gen)} generated rows, expected {expected}"
        )


if __name__ == "__main__":
    main()
