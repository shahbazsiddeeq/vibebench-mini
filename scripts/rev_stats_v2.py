#!/usr/bin/env python3.12
"""Statistical analysis for CodeAssay, revision 2.

Replaces scripts/rev_stats.py. Three methodological corrections drive this file.

Item 7. Correctness under the strict gate is BINARY per task (a solution either
passes all of a task's hidden tests or it does not). Wilcoxon signed-rank and
Cliff's delta are the wrong instruments for paired binary data: the signed-rank
statistic degenerates because every non-zero difference has the same magnitude,
and Cliff's delta on a two-valued variable only re-encodes the discordant-pair
proportion. We therefore use Cochran's Q for the omnibus test across models and
exact McNemar tests on discordant pairs for the pairwise contrasts, with
Holm-Bonferroni correction, and report the risk difference with a confidence
interval as the effect size.

Item 2. Quality indicators may only be compared on tasks solved correctly by
BOTH configurations being compared. Comparing each configuration's quality mean
over its own passing set compares different task samples, and the extra tasks a
stronger model solves are the harder ones. Every quality comparison here is
restricted to a jointly-correct set, and the size of that set is reported.

Item 3. The three normalized quality scores are retired. They were

    lint_score       = max(0, 1 - min(flake8_count, 20) / 20)
    security_score   = max(0, 1 - min(bandit_count, 20) / 20)
    complexity_score = 1 if cc <= 5 else (0 if cc >= 15 else 1 - (cc - 5) / 10)

The style score was a raw violation count, so it measured program length as much
as style, and censoring at 20 discarded the tail. The security score collapsed
Bandit findings of different severities into one number and censored it the same
way. The complexity score was a piecewise-linear rescaling whose knees at 5 and
15 have no basis in the literature we cite. They are replaced by

    style        flake8 violations per 100 logical lines (radon lloc),
                 reported for all violations and excluding whitespace-only codes
    complexity   raw mean cyclomatic complexity (primary), raw maximum (secondary)
    security     Bandit and Semgrep finding counts BY SEVERITY, descriptive only;
                 no security score is computed and none is tested

The raw measurements come from reports/quality_remeasured.csv, produced by
scripts/remeasure_quality.py, which re-runs flake8, Bandit, radon and Semgrep on
the stored solutions and reproduces the runner's stored flake8 and Bandit totals
exactly.

Outputs:
  reports/rev_stats_v2.md                   human-readable report
  reports/rev_quality_common14.csv          per-config quality on the 14-way set
  reports/rev_quality_jointly_correct.csv   per-config quality, std prompt, 7-way set
  reports/rev_pairwise_correctness.csv      all pairwise McNemar contrasts

The corpus is selected with --runs-prefix. The default, "r2-", is the released
corpus: it reads .agent_runs/r2-<slug>-<prompt> and
reports/r2_quality_remeasured.csv, and writes reports/r2_rev_stats.md,
reports/r2_quality_common14.csv, reports/r2_quality_jointly_correct.csv and
reports/r2_pairwise_correctness.csv. An empty prefix names the superseded
pre-revision corpus and reproduces the unprefixed file names above; those runs
are not part of the public artifact.

Correctness comes from --correctness. `results` reads the `correctness` column of
.agent_runs/<config>/results.csv and applies the strict gate correctness >= 1.0.
`audit` reads the `final_hidden_pass` column of reports/<tag>_repair_audit.csv,
which is the correctness source for the r2 corpus, whose scoring runners were
stopped and which therefore has no results.csv. `auto`, the default, uses
results.csv when it exists and the audit otherwise. No statistical method changes
with the source: the omnibus test is still Cochran's Q, the pairwise contrasts
are still exact McNemar with Holm correction, the paired quality tests are still
Wilcoxon with the Pratt convention with a matched-pairs rank-biserial effect size
computed under that same convention, proportions still get Wilson intervals and
means still get a 10,000-resample percentile bootstrap.

Run:  python3.12 scripts/rev_stats_v2.py
      python3.12 scripts/rev_stats_v2.py --runs-prefix '' --correctness results
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / ".agent_runs"
REPORTS = ROOT / "reports"
TASKS = ROOT / "tasks" / "python"

# Set from the command line in main(). RUNS_PREFIX selects the corpus, TAG is the
# file-name stem derived from it, and CORRECTNESS is the correctness source.
RUNS_PREFIX = ""
TAG = ""
CORRECTNESS = "auto"

# Display order is by capability tier, matching the paper's table.
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

# The corrected quality indicators. Lower is better for every one of them.
QUALITY = [
    ("style_per100_lloc", "Style /100 lloc"),
    ("style_nonws_per100_lloc", "Style excl. ws /100 lloc"),
    ("cc_mean", "Mean CC (raw)"),
    ("cc_max", "Max CC (raw)"),
    ("lloc", "Logical lines"),
]
# The subset the paper tests. Length is reported but not tested as a quality
# claim; it is reported because it is the denominator of the style indicator.
TESTED = ["style_per100_lloc", "style_nonws_per100_lloc", "cc_mean", "cc_max"]

WHITESPACE_CODES = ["W291", "W293", "W391", "E303"]

RNG = np.random.default_rng(20260731)
N_BOOT = 10000


# --------------------------------------------------------------------------
# corpus paths
# --------------------------------------------------------------------------
def out_path(stem: str) -> Path:
    """reports/<stem> for the original corpus, reports/<TAG>_<stem> otherwise."""
    return REPORTS / (f"{TAG}_{stem}" if TAG else stem)


def report_paths() -> dict[str, Path]:
    """Output file names. The original corpus keeps its historical names."""
    if not TAG:
        return {
            "md": REPORTS / "rev_stats_v2.md",
            "common14": REPORTS / "rev_quality_common14.csv",
            "jointly": REPORTS / "rev_quality_jointly_correct.csv",
            "pairwise": REPORTS / "rev_pairwise_correctness.csv",
        }
    return {
        "md": REPORTS / f"{TAG}_rev_stats.md",
        "common14": REPORTS / f"{TAG}_quality_common14.csv",
        "jointly": REPORTS / f"{TAG}_quality_jointly_correct.csv",
        "pairwise": REPORTS / f"{TAG}_pairwise_correctness.csv",
    }


def remeasured_path() -> Path:
    return out_path("quality_remeasured.csv")


def audit_path() -> Path:
    return out_path("repair_audit.csv")


def use_audit() -> bool:
    """True when correctness must come from the repair audit."""
    if CORRECTNESS in ("audit", "results"):
        return CORRECTNESS == "audit"
    probe = RUNS / f"{RUNS_PREFIX}{MODELS[0][0]}-{PROMPTS[0]}" / "results.csv"
    return not probe.exists()


# --------------------------------------------------------------------------
# data loading
# --------------------------------------------------------------------------
def load_config(slug: str, prompt: str) -> dict[str, dict]:
    """Return {task_id: row} for one configuration, aggregate row dropped."""
    path = RUNS / f"{RUNS_PREFIX}{slug}-{prompt}" / "results.csv"
    if not path.exists():
        raise SystemExit(f"missing results file: {path}")
    out = {}
    with path.open() as fh:
        for row in csv.DictReader(fh):
            if row["id"] == "__aggregate__":
                continue
            out[row["id"]] = row
    return out


def load_audit() -> dict[tuple[str, str], dict[str, dict]]:
    """Return {(slug, prompt): {task: audit row}} from the repair audit CSV.

    The audit carries one row per configuration and task. `final_hidden_pass` is
    the outcome of the final program against the hidden suite, which is exactly
    the strict-gate quantity results.csv's `correctness >= 1.0` encoded for the
    original corpus.
    """
    path = audit_path()
    if not path.exists():
        raise SystemExit(f"missing correctness source: {path}")
    out: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    with path.open() as fh:
        for row in csv.DictReader(fh):
            run = row["run"]
            body = run[len(RUNS_PREFIX):] if RUNS_PREFIX and run.startswith(RUNS_PREFIX) else run
            slug, _, prompt = body.rpartition("-")
            out[(slug, prompt)][row["task"]] = row
    return out


def to_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_remeasured() -> dict[str, dict[str, dict]]:
    """Return {config_key: {task: row}} from the re-measured quality CSV."""
    path = remeasured_path()
    if not path.exists():
        raise SystemExit(
            f"missing {path}; run python3.12 scripts/remeasure_quality.py "
            f"--runs-prefix {RUNS_PREFIX!r} first"
        )
    out: dict[str, dict[str, dict]] = defaultdict(dict)
    with path.open() as fh:
        for row in csv.DictReader(fh):
            out[row["config"]][row["task"]] = row
    return out


def build_matrices():
    """Return (tasks, correct, quality, meas).

    correct[(slug, prompt)] -> np.array of 0/1 aligned to `tasks`
    quality[(slug, prompt)][metric] -> np.array of float/nan aligned to `tasks`
    meas[(slug, prompt)][col] -> np.array of float/nan for auxiliary raw columns
    """
    from_audit = use_audit()
    raw = {}
    if from_audit:
        audit = load_audit()
        for slug, _ in MODELS:
            for prompt in PROMPTS:
                rows = audit.get((slug, prompt))
                if not rows:
                    raise SystemExit(
                        f"no rows for {RUNS_PREFIX}{slug}-{prompt} in {audit_path()}"
                    )
                raw[(slug, prompt)] = rows
    else:
        for slug, _ in MODELS:
            for prompt in PROMPTS:
                raw[(slug, prompt)] = load_config(slug, prompt)

    rem = load_remeasured()

    task_sets = [set(v) for v in raw.values()]
    tasks = sorted(set.intersection(*task_sets))
    if len(tasks) != 185:
        print(f"note: {len(tasks)} tasks common to all configurations")

    aux_cols = [
        "flake8_total", "flake8_ws", "flake8_nonws", "sloc", "raw_loc",
        "bandit_total", "bandit_high", "bandit_medium", "bandit_low",
        "semgrep_total", "semgrep_error", "semgrep_warning", "semgrep_info",
        *[f"flake8_{c}" for c in WHITESPACE_CODES],
    ]

    correct, quality, meas = {}, {}, {}
    for (slug, prompt), rows in raw.items():
        key = (slug, prompt)
        cfg = f"{slug}-{prompt}"
        if from_audit:
            c = np.array(
                [1 if rows[t]["final_hidden_pass"] == "True" else 0 for t in tasks],
                dtype=int,
            )
        else:
            c = np.array(
                [1 if (to_float(rows[t]["correctness"]) or 0.0) >= 1.0 else 0 for t in tasks],
                dtype=int,
            )
        correct[key] = c
        rr = rem.get(cfg, {})
        quality[key] = {}
        for col, _ in QUALITY:
            quality[key][col] = np.array(
                [to_float((rr.get(t) or {}).get(col)) for t in tasks], dtype=object
            )
            quality[key][col] = np.array(
                [np.nan if v is None else float(v) for v in quality[key][col]],
                dtype=float,
            )
        meas[key] = {}
        for col in aux_cols:
            vals = [to_float((rr.get(t) or {}).get(col)) for t in tasks]
            meas[key][col] = np.array(
                [np.nan if v is None else v for v in vals], dtype=float
            )
        # legacy normalized scores, retained only so the deprecated figure
        # script keeps running; not analysed anywhere below
        for col in ("complexity_score", "lint_score", "security_score"):
            vals = [to_float(rows[t].get(col)) for t in tasks]
            meas[key][col] = np.array(
                [np.nan if v is None else v for v in vals], dtype=float
            )
        # per-code flake8 counters, for the whitespace composition table
        meas[key]["codes"] = [
            parse_codes((rr.get(t) or {}).get("flake8_codes", "")) for t in tasks
        ]
        meas[key]["bandit_tests"] = [
            parse_codes((rr.get(t) or {}).get("bandit_tests", "")) for t in tasks
        ]
    return tasks, correct, quality, meas


def parse_codes(s: str) -> Counter:
    c: Counter = Counter()
    for part in (s or "").split(";"):
        if ":" in part:
            k, v = part.rsplit(":", 1)
            try:
                c[k] += int(v)
            except ValueError:
                pass
    return c


def load_reference() -> dict[str, dict]:
    rem = load_remeasured()
    return rem.get("reference", {})


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------
def wilson_ci(k: int, n: int, conf: float = 0.95):
    """Wilson score interval for a binomial proportion, in percent.

    Preferred over a bootstrap for a proportion: it is exact in coverage terms
    at these sample sizes and does not collapse when the proportion nears 1,
    which matters here because several configurations exceed 98 percent.
    """
    if n == 0:
        return (float("nan"), float("nan"))
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (100 * max(0.0, centre - half), 100 * min(1.0, centre + half))


def cochrans_q(mat: np.ndarray):
    """Cochran's Q for k related binary samples. mat is (n_tasks, k)."""
    n, k = mat.shape
    col = mat.sum(axis=0).astype(float)
    row = mat.sum(axis=1).astype(float)
    num = (k - 1) * (k * np.sum(col**2) - col.sum() ** 2)
    den = k * row.sum() - np.sum(row**2)
    if den == 0:
        return 0.0, k - 1, 1.0
    q = num / den
    df = k - 1
    return q, df, float(stats.chi2.sf(q, df))


def mcnemar_exact(a: np.ndarray, b: np.ndarray):
    """Exact two-sided McNemar test on paired binary outcomes.

    Returns (b_count, c_count, p_value) where b_count is the number of tasks a
    solved and b did not, and c_count the reverse. Concordant pairs carry no
    information about a difference and are excluded by construction.
    """
    b_cnt = int(np.sum((a == 1) & (b == 0)))
    c_cnt = int(np.sum((a == 0) & (b == 1)))
    if b_cnt + c_cnt == 0:
        return b_cnt, c_cnt, 1.0
    p = stats.binomtest(b_cnt, b_cnt + c_cnt, 0.5, alternative="two-sided").pvalue
    return b_cnt, c_cnt, float(p)


def holm(pvals: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values, monotonicity enforced."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        val = min(1.0, (m - rank) * pvals[idx])
        running = max(running, val)
        adj[idx] = running
    return adj


def risk_difference_ci(a: np.ndarray, b: np.ndarray, conf: float = 0.95):
    """Paired risk difference (a - b) in percentage points, with a Wald CI
    based on the discordant counts (Agresti-Min style for matched pairs)."""
    n = len(a)
    b_cnt = int(np.sum((a == 1) & (b == 0)))
    c_cnt = int(np.sum((a == 0) & (b == 1)))
    diff = (b_cnt - c_cnt) / n
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    var = (b_cnt + c_cnt - (b_cnt - c_cnt) ** 2 / n) / (n * n)
    half = z * math.sqrt(max(var, 0.0))
    return 100 * diff, 100 * (diff - half), 100 * (diff + half)


def boot_mean_ci(x: np.ndarray, conf: float = 0.95):
    """Percentile bootstrap CI for a mean."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    if len(x) == 1:
        return float(x[0]), float(x[0]), float(x[0])
    idx = RNG.integers(0, len(x), size=(N_BOOT, len(x)))
    means = x[idx].mean(axis=1)
    lo, hi = np.percentile(means, [100 * (1 - conf) / 2, 100 * (1 + conf) / 2])
    return float(x.mean()), float(lo), float(hi)


def boot_ratio_ci(num: np.ndarray, den: np.ndarray, conf: float = 0.95):
    """Percentile bootstrap CI for a ratio of sums, resampling tasks.

    Used for the pooled style rate (total violations / total logical lines),
    which is the length-weighted counterpart of the mean of per-task rates.
    """
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    ok = ~(np.isnan(num) | np.isnan(den))
    num, den = num[ok], den[ok]
    if len(num) == 0 or den.sum() == 0:
        return float("nan"), float("nan"), float("nan")
    point = 100 * num.sum() / den.sum()
    idx = RNG.integers(0, len(num), size=(N_BOOT, len(num)))
    ratios = 100 * num[idx].sum(axis=1) / den[idx].sum(axis=1)
    lo, hi = np.percentile(ratios, [100 * (1 - conf) / 2, 100 * (1 + conf) / 2])
    return float(point), float(lo), float(hi)


def paired_wilcoxon(x: np.ndarray, y: np.ndarray):
    """Paired Wilcoxon signed-rank with Pratt zero handling, plus the
    matched-pairs rank-biserial correlation as the effect size.

    Returns dict with n, n_zero (tied pairs), p, r_rb, median difference.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    d = x - y
    n_zero = int(np.sum(d == 0))
    out = {
        "n": n,
        "n_zero": n_zero,
        "mean_diff": float(np.mean(d)) if n else float("nan"),
        "median_diff": float(np.median(d)) if n else float("nan"),
        "p": float("nan"),
        "r_rb": float("nan"),
    }
    if n == 0 or np.all(d == 0):
        out["p"] = 1.0
        out["r_rb"] = 0.0
        return out
    try:
        out["p"] = float(stats.wilcoxon(x, y, zero_method="pratt").pvalue)
    except ValueError:
        out["p"] = 1.0
    # Matched-pairs rank-biserial correlation, computed CONSISTENTLY with the
    # Pratt p-value above. Pratt ranks the absolute differences with the zero
    # differences included, then excludes the zeros from the rank sums. Ranking
    # only the non-zero differences (the Wilcoxon convention) would inflate the
    # effect size relative to the test that produced the p-value, so the
    # normaliser is n(n+1)/2 over all n pairs including ties.
    ranks = stats.rankdata(np.abs(d))
    r_pos = float(ranks[d > 0].sum())
    r_neg = float(ranks[d < 0].sum())
    out["r_rb"] = (r_pos - r_neg) / (n * (n + 1) / 2)
    return out


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
def fmt_p(p: float) -> str:
    if p != p:
        return "n/a"
    if p < 1e-3:
        return "<0.001"
    return f"{p:.3f}"


def main() -> None:
    global RUNS_PREFIX, TAG, CORRECTNESS
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-prefix", default="r2-",
                    help="prefix of the .agent_runs configuration directories; "
                         "'r2-' is the released corpus, '' the superseded "
                         "pre-revision one, which is not part of the public "
                         "artifact")
    ap.add_argument("--correctness", choices=["auto", "results", "audit"],
                    default="auto",
                    help="correctness source: results.csv, the repair audit's "
                         "final_hidden_pass column, or whichever is present")
    args = ap.parse_args()
    RUNS_PREFIX = args.runs_prefix
    TAG = RUNS_PREFIX.strip("-")
    CORRECTNESS = args.correctness

    REPORTS.mkdir(exist_ok=True)
    OUT = report_paths()
    src = "the repair audit's final_hidden_pass column" if use_audit() else "results.csv"
    print(f"corpus prefix {RUNS_PREFIX!r}; correctness from {src}")
    tasks, correct, quality, meas = build_matrices()
    reference = load_reference()
    n_tasks = len(tasks)
    L: list[str] = []

    def w(s: str = "") -> None:
        L.append(s)

    w("# CodeAssay statistics, revision 2")
    w()
    if RUNS_PREFIX:
        provenance = (
            f"Generated by `scripts/rev_stats_v2.py --runs-prefix {RUNS_PREFIX}` from "
            f"`reports/{remeasured_path().name}` (`scripts/remeasure_quality.py`) over "
            f"the `{RUNS_PREFIX}` corpus, with correctness taken from the "
            f"`final_hidden_pass` column of `reports/{audit_path().name}`. "
        )
    else:
        provenance = (
            "Generated by `scripts/rev_stats_v2.py` from "
            "`reports/quality_remeasured.csv` (`scripts/remeasure_quality.py`) and "
            "the stored per-task results. "
        )
    w(
        provenance
        + "Correctness is binary per task (passes all hidden tests or not), so the "
        "omnibus test is Cochran's Q and the pairwise contrasts are exact McNemar "
        "tests with Holm-Bonferroni correction. Every quality comparison is "
        "restricted to tasks solved correctly by both configurations being compared."
    )
    w()
    w("## Measurement definitions")
    w()
    w(
        "The three normalized quality scores used previously are withdrawn. The "
        "style score was a raw flake8 count censored at 20, so it grew with program "
        "length and discarded the tail; the security score collapsed Bandit findings "
        "of different severities into one censored number; the complexity score was "
        "a piecewise rescaling with unjustified knees at 5 and 15. The replacements:"
    )
    w()
    w("| Indicator | Definition | Direction |")
    w("|---|---|---|")
    w("| Style | flake8 violations per 100 logical lines (radon `lloc`), "
      "flake8 at max-line-length 120 | lower is better |")
    w("| Style, excl. whitespace | the same, dropping W291, W293, W391 and E303 | lower is better |")
    w("| Complexity (primary) | raw mean cyclomatic complexity over the file's blocks | lower is better |")
    w("| Complexity (secondary) | raw maximum cyclomatic complexity in the file | lower is better |")
    w("| Security | Bandit and Semgrep finding counts by severity | descriptive, not scored |")
    w()
    w(
        "No security score is computed and no significance test is run on the "
        "security counts: the counts are near zero for every configuration and a "
        "test on them would be uninterpretable. They are reported as counts."
    )
    w()
    w(f"Tasks: {n_tasks}. Configurations: {len(MODELS)} models x {len(PROMPTS)} prompts.")
    w()

    # ---------------- RQ1 correctness ----------------
    w("## RQ1. Correctness across the seven models (standard prompt)")
    w()
    w("| Model | pass (%) | k/n | Wilson 95% CI |")
    w("|---|---|---|---|")
    for slug, name in MODELS:
        c = correct[(slug, "std")]
        k = int(c.sum())
        lo, hi = wilson_ci(k, n_tasks)
        w(f"| {name} | {100*k/n_tasks:.1f} | {k}/{n_tasks} | [{lo:.1f}, {hi:.1f}] |")
    w()

    mat = np.column_stack([correct[(slug, "std")] for slug, _ in MODELS])
    q, df, p = cochrans_q(mat)
    w(f"Cochran's Q = {q:.1f}, df = {df}, p = {fmt_p(p)}.")
    w()

    pairs, praw = [], []
    for (s1, n1), (s2, n2) in combinations(MODELS, 2):
        a, b = correct[(s1, "std")], correct[(s2, "std")]
        bc, cc, pv = mcnemar_exact(a, b)
        rd, rlo, rhi = risk_difference_ci(a, b)
        pairs.append((n1, n2, bc, cc, rd, rlo, rhi))
        praw.append(pv)
    padj = holm(praw)

    w("### Pairwise exact McNemar, Holm-corrected")
    w()
    w(
        "b = tasks the first model solved and the second did not; c = the reverse. "
        "RD = paired risk difference in percentage points."
    )
    w()
    w("| Model A | Model B | b | c | RD (pp) | 95% CI | p | Holm p | sig. |")
    w("|---|---|---|---|---|---|---|---|---|")
    rows_pair = []
    for (n1, n2, bc, cc, rd, rlo, rhi), pv, pa in zip(pairs, praw, padj):
        sig = "yes" if pa < 0.05 else "no"
        w(
            f"| {n1} | {n2} | {bc} | {cc} | {rd:+.1f} | [{rlo:+.1f}, {rhi:+.1f}] | "
            f"{fmt_p(pv)} | {fmt_p(pa)} | {sig} |"
        )
        rows_pair.append(
            {
                "model_a": n1, "model_b": n2, "b": bc, "c": cc,
                "risk_diff_pp": round(rd, 2), "ci_lo": round(rlo, 2),
                "ci_hi": round(rhi, 2), "p_exact": pv, "p_holm": pa,
                "significant": sig,
            }
        )
    w()
    n_sig = sum(1 for r in rows_pair if r["significant"] == "yes")
    w(f"Significant after Holm correction: {n_sig} of {len(rows_pair)} contrasts.")
    w()

    with OUT["pairwise"].open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows_pair[0]))
        wr.writeheader()
        wr.writerows(rows_pair)

    # ---------------- the analysis sets ----------------
    common7 = np.ones(n_tasks, dtype=bool)
    for slug, _ in MODELS:
        common7 &= correct[(slug, "std")] == 1
    n_common7 = int(common7.sum())

    common14 = np.ones(n_tasks, dtype=bool)
    for slug, _ in MODELS:
        for prompt in PROMPTS:
            common14 &= correct[(slug, prompt)] == 1
    n14 = int(common14.sum())

    # ---------------- RQ1 quality on the 14-way common set ----------------
    w("## RQ1. Quality indicators on the set solved by all 14 configurations")
    w()
    w(
        f"All 14 configurations solve {n14} of {n_tasks} tasks in common. Every "
        "quality number in this section is computed on exactly this set, so each "
        "model is scored on the same task set. Correctness itself is still "
        f"reported over all {n_tasks} tasks. The seven standard-prompt "
        f"configurations alone share {n_common7} tasks; the smaller 14-way set is "
        "used throughout so that the RQ1 and RQ2 tables rest on the same task set."
    )
    w()
    w("### Style, complexity and length (standard prompt)")
    w()
    w(
        "`Style` is the mean over tasks of the per-task rate. `Pooled` is the "
        "length-weighted rate, total violations over total logical lines, which "
        "removes the influence of short files on the unweighted mean."
    )
    w()
    w("| Model | lloc | Style /100 lloc | 95% CI | Pooled | 95% CI | "
      "Excl. ws /100 lloc | 95% CI | Mean CC | 95% CI | Max CC | 95% CI |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for slug, name in MODELS:
        Q = quality[(slug, "std")]
        M = meas[(slug, "std")]
        lloc = float(np.nanmean(Q["lloc"][common14]))
        s_m, s_lo, s_hi = boot_mean_ci(Q["style_per100_lloc"][common14])
        p_m, p_lo, p_hi = boot_ratio_ci(M["flake8_total"][common14], Q["lloc"][common14])
        n_m, n_lo, n_hi = boot_mean_ci(Q["style_nonws_per100_lloc"][common14])
        c_m, c_lo, c_hi = boot_mean_ci(Q["cc_mean"][common14])
        x_m, x_lo, x_hi = boot_mean_ci(Q["cc_max"][common14])
        w(
            f"| {name} | {lloc:.1f} | {s_m:.2f} | [{s_lo:.2f}, {s_hi:.2f}] | "
            f"{p_m:.2f} | [{p_lo:.2f}, {p_hi:.2f}] | "
            f"{n_m:.2f} | [{n_lo:.2f}, {n_hi:.2f}] | "
            f"{c_m:.2f} | [{c_lo:.2f}, {c_hi:.2f}] | "
            f"{x_m:.2f} | [{x_lo:.2f}, {x_hi:.2f}] |"
        )
    ref_idx = [t for i, t in enumerate(tasks) if common14[i]]
    ref_style = np.array([to_float(reference[t]["style_per100_lloc"]) for t in ref_idx if t in reference], dtype=float)
    ref_nonws = np.array(
        [to_float(reference[t]["style_nonws_per100_lloc"]) for t in ref_idx if t in reference],
        dtype=float,
    )
    ref_ccm = np.array([to_float(reference[t]["cc_mean"]) for t in ref_idx if t in reference], dtype=float)
    ref_ccx = np.array([to_float(reference[t]["cc_max"]) for t in ref_idx if t in reference], dtype=float)
    ref_lloc = np.array([to_float(reference[t]["lloc"]) for t in ref_idx if t in reference], dtype=float)
    ref_f8 = np.array([to_float(reference[t]["flake8_total"]) for t in ref_idx if t in reference], dtype=float)
    if len(ref_style):
        s_m, s_lo, s_hi = boot_mean_ci(ref_style)
        p_m, p_lo, p_hi = boot_ratio_ci(ref_f8, ref_lloc)
        n_m, n_lo, n_hi = boot_mean_ci(ref_nonws)
        c_m, c_lo, c_hi = boot_mean_ci(ref_ccm)
        x_m, x_lo, x_hi = boot_mean_ci(ref_ccx)
        w(
            f"| CodeAssay reference | {np.nanmean(ref_lloc):.1f} | {s_m:.2f} | [{s_lo:.2f}, {s_hi:.2f}] | "
            f"{p_m:.2f} | [{p_lo:.2f}, {p_hi:.2f}] | {n_m:.2f} | [{n_lo:.2f}, {n_hi:.2f}] | "
            f"{c_m:.2f} | [{c_lo:.2f}, {c_hi:.2f}] | {x_m:.2f} | [{x_lo:.2f}, {x_hi:.2f}] |"
        )
    w()

    # whitespace composition
    w("### Composition of the style violations (standard prompt, same set)")
    w()
    w(
        "Total violations over the whole set, then the share contributed by the "
        "whitespace-only codes. These four codes are removed by any autoformatter, "
        "so a style ranking that they dominate is a ranking of formatter usage."
    )
    w()
    w("| Model | Total | W293 | W291 | W391 | E303 | Whitespace | "
      "Whitespace share (%) | W293 share (%) | Top non-whitespace codes |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    ws_rows = {}
    for slug, name in MODELS:
        M = meas[(slug, "std")]
        tot = float(np.nansum(M["flake8_total"][common14]))
        ws = float(np.nansum(M["flake8_ws"][common14]))
        per = {c: float(np.nansum(M[f"flake8_{c}"][common14])) for c in WHITESPACE_CODES}
        agg: Counter = Counter()
        for i, keep in enumerate(common14):
            if keep:
                agg.update(M["codes"][i])
        nonws = Counter({k: v for k, v in agg.items() if k not in WHITESPACE_CODES})
        top = ", ".join(f"{k} {v}" for k, v in nonws.most_common(4)) or "none"
        ws_rows[name] = (tot, ws, per, nonws)
        w(
            f"| {name} | {tot:.0f} | {per['W293']:.0f} | {per['W291']:.0f} | "
            f"{per['W391']:.0f} | {per['E303']:.0f} | {ws:.0f} | "
            f"{100*ws/tot if tot else float('nan'):.1f} | "
            f"{100*per['W293']/tot if tot else float('nan'):.1f} | {top} |"
        )
    w()

    # pairwise Wilcoxon on the 14-way set
    for col in ("style_per100_lloc", "cc_mean"):
        lab = dict(QUALITY)[col]
        w(f"### {lab}: pairwise paired Wilcoxon on the {n14}-task set (standard prompt)")
        w()
        w("| Model A | Model B | n | ties | mean diff | r (rank-biserial) | p | Holm p |")
        w("|---|---|---|---|---|---|---|---|")
        recs, pr = [], []
        for (s1, n1), (s2, n2) in combinations(MODELS, 2):
            r = paired_wilcoxon(
                quality[(s1, "std")][col][common14], quality[(s2, "std")][col][common14]
            )
            recs.append((n1, n2, r))
            pr.append(r["p"])
        pa = holm(pr)
        for (n1, n2, r), a in zip(recs, pa):
            w(
                f"| {n1} | {n2} | {r['n']} | {r['n_zero']} | {r['mean_diff']:+.3f} | "
                f"{r['r_rb']:+.2f} | {fmt_p(r['p'])} | {fmt_p(a)} |"
            )
        w()

    # ---------------- main table CSV ----------------
    rows14 = []
    for slug, name in MODELS:
        for prompt in PROMPTS:
            Q = quality[(slug, prompt)]
            M = meas[(slug, prompt)]
            rec = {"model": name, "prompt": prompt, "n_common14": n14}
            for col, _ in QUALITY:
                m, lo, hi = boot_mean_ci(Q[col][common14])
                rec[f"{col}_mean"] = round(m, 6)
                rec[f"{col}_lo"] = round(lo, 6)
                rec[f"{col}_hi"] = round(hi, 6)
            pm, plo, phi = boot_ratio_ci(M["flake8_total"][common14], Q["lloc"][common14])
            rec["style_pooled_per100_lloc"] = round(pm, 6)
            rec["style_pooled_lo"] = round(plo, 6)
            rec["style_pooled_hi"] = round(phi, 6)
            rec["flake8_total_sum"] = int(np.nansum(M["flake8_total"][common14]))
            rec["flake8_ws_sum"] = int(np.nansum(M["flake8_ws"][common14]))
            rec["flake8_W293_sum"] = int(np.nansum(M["flake8_W293"][common14]))
            rec["ws_share_pct"] = round(
                100 * rec["flake8_ws_sum"] / rec["flake8_total_sum"], 2
            ) if rec["flake8_total_sum"] else ""
            for b in ("bandit_total", "bandit_high", "bandit_medium", "bandit_low"):
                rec[f"{b}_sum"] = int(np.nansum(M[b][common14]))
            for s in ("semgrep_total", "semgrep_error", "semgrep_warning", "semgrep_info"):
                rec[f"{s}_sum"] = int(np.nansum(M[s][common14]))
            # deprecated normalized scores, kept only for the legacy figure script
            for col in ("complexity_score", "lint_score", "security_score"):
                m, lo, hi = boot_mean_ci(M[col][common14])
                rec[f"{col}_mean"] = round(m, 6)
                rec[f"{col}_lo"] = round(lo, 6)
                rec[f"{col}_hi"] = round(hi, 6)
            rows14.append(rec)
    with OUT["common14"].open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows14[0]))
        wr.writeheader()
        wr.writerows(rows14)

    # standard-prompt 7-way set, kept for continuity
    qrows = []
    for slug, name in MODELS:
        rec = {"model": name, "n_common7": n_common7}
        for col, _ in QUALITY:
            m, lo, hi = boot_mean_ci(quality[(slug, "std")][col][common7])
            rec[f"{col}_mean"] = round(m, 6)
            rec[f"{col}_lo"] = round(lo, 6)
            rec[f"{col}_hi"] = round(hi, 6)
        qrows.append(rec)
    with OUT["jointly"].open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(qrows[0]))
        wr.writeheader()
        wr.writerows(qrows)

    # ---------------- security, descriptive ----------------
    w("## Security findings, descriptive (no score, no test)")
    w()
    w(f"### Bandit by severity on the {n14}-task set")
    w()
    w(
        "Counts are totals over the set, not per-file means. `Files` is the number "
        "of solutions with at least one finding. The reference column is the "
        f"benchmark's own {len(reference)} reference solutions, scanned identically."
    )
    w()
    w("| Configuration | Prompt | HIGH | MEDIUM | LOW | Total | Files w/ finding | Most frequent tests |")
    w("|---|---|---|---|---|---|---|---|")
    for slug, name in MODELS:
        for prompt in PROMPTS:
            M = meas[(slug, prompt)]
            hi_ = int(np.nansum(M["bandit_high"][common14]))
            me = int(np.nansum(M["bandit_medium"][common14]))
            lo_ = int(np.nansum(M["bandit_low"][common14]))
            tot = int(np.nansum(M["bandit_total"][common14]))
            nf = int(np.nansum(M["bandit_total"][common14] > 0))
            agg: Counter = Counter()
            for i, keep in enumerate(common14):
                if keep:
                    agg.update(M["bandit_tests"][i])
            top = ", ".join(f"{k} {v}" for k, v in agg.most_common(4)) or "none"
            w(f"| {name} | {prompt} | {hi_} | {me} | {lo_} | {tot} | {nf} | {top} |")
    # reference rows
    for label, subset in (
        (f"same {len(ref_idx)} tasks", ref_idx),
        (f"all {len(reference)} tasks", sorted(reference)),
    ):
        hi_ = sum(int(to_float(reference[t]["bandit_high"]) or 0) for t in subset if t in reference)
        me = sum(int(to_float(reference[t]["bandit_medium"]) or 0) for t in subset if t in reference)
        lo_ = sum(int(to_float(reference[t]["bandit_low"]) or 0) for t in subset if t in reference)
        tot = sum(int(to_float(reference[t]["bandit_total"]) or 0) for t in subset if t in reference)
        nf = sum(1 for t in subset if t in reference and (to_float(reference[t]["bandit_total"]) or 0) > 0)
        agg = Counter()
        for t in subset:
            if t in reference:
                agg.update(parse_codes(reference[t]["bandit_tests"]))
        top = ", ".join(f"{k} {v}" for k, v in agg.most_common(4)) or "none"
        w(f"| CodeAssay reference | {label} | {hi_} | {me} | {lo_} | {tot} | {nf} | {top} |")
    w()

    w("### Bandit by severity over all 185 tasks (every stored solution)")
    w()
    w("| Configuration | Prompt | Files | HIGH | MEDIUM | LOW | Total |")
    w("|---|---|---|---|---|---|---|")
    for slug, name in MODELS:
        for prompt in PROMPTS:
            M = meas[(slug, prompt)]
            nf = int(np.sum(~np.isnan(M["bandit_total"])))
            w(
                f"| {name} | {prompt} | {nf} | "
                f"{int(np.nansum(M['bandit_high']))} | {int(np.nansum(M['bandit_medium']))} | "
                f"{int(np.nansum(M['bandit_low']))} | {int(np.nansum(M['bandit_total']))} |"
            )
    hi_ = sum(int(to_float(r["bandit_high"]) or 0) for r in reference.values())
    me = sum(int(to_float(r["bandit_medium"]) or 0) for r in reference.values())
    lo_ = sum(int(to_float(r["bandit_low"]) or 0) for r in reference.values())
    tot = sum(int(to_float(r["bandit_total"]) or 0) for r in reference.values())
    w(f"| CodeAssay reference | n/a | {len(reference)} | {hi_} | {me} | {lo_} | {tot} |")
    w()

    w("### Semgrep by severity over all 185 tasks")
    w()
    w(
        "Semgrep Registry packs `p/python` and `p/security-audit`, default "
        "severities, no local rules; see `reports/semgrep_summary.md`."
    )
    w()
    w("| Configuration | Prompt | ERROR | WARNING | INFO | Total |")
    w("|---|---|---|---|---|---|")
    for slug, name in MODELS:
        for prompt in PROMPTS:
            M = meas[(slug, prompt)]
            w(
                f"| {name} | {prompt} | {int(np.nansum(M['semgrep_error']))} | "
                f"{int(np.nansum(M['semgrep_warning']))} | {int(np.nansum(M['semgrep_info']))} | "
                f"{int(np.nansum(M['semgrep_total']))} |"
            )
    se = sum(int(to_float(r["semgrep_error"]) or 0) for r in reference.values())
    sw = sum(int(to_float(r["semgrep_warning"]) or 0) for r in reference.values())
    si = sum(int(to_float(r["semgrep_info"]) or 0) for r in reference.values())
    w(f"| CodeAssay reference | n/a | {se} | {sw} | {si} | {se+sw+si} |")
    w()

    # ---------------- RQ2 ----------------
    w("## RQ2. Security-focused prompt versus standard prompt (paired, within model)")
    w()
    w("### Correctness (exact McNemar)")
    w()
    w("| Model | std (%) | sec (%) | b (std only) | c (sec only) | RD (pp) | 95% CI | p | Holm p |")
    w("|---|---|---|---|---|---|---|---|---|")
    recs, pr = [], []
    for slug, name in MODELS:
        a, b = correct[(slug, "std")], correct[(slug, "sec")]
        bc, cc, pv = mcnemar_exact(a, b)
        rd, rlo, rhi = risk_difference_ci(a, b)
        recs.append((name, a.sum(), b.sum(), bc, cc, rd, rlo, rhi))
        pr.append(pv)
    pa = holm(pr)
    for (name, ka, kb, bc, cc, rd, rlo, rhi), pv, a in zip(recs, pr, pa):
        w(
            f"| {name} | {100*ka/n_tasks:.1f} | {100*kb/n_tasks:.1f} | {bc} | {cc} | "
            f"{rd:+.1f} | [{rlo:+.1f}, {rhi:+.1f}] | {fmt_p(pv)} | {fmt_p(a)} |"
        )
    w()

    w("### Quality on each model's jointly-correct set")
    w()
    w(
        "Each row is a paired comparison on the tasks that model solved under both "
        "prompts. `diff` is sec minus std, so a positive difference means the "
        "security-focused prompt made the indicator worse. Holm correction is "
        "applied across the seven models within each metric (family size 7)."
    )
    w()
    both_idx = {}
    for slug, _ in MODELS:
        both_idx[slug] = (correct[(slug, "std")] == 1) & (correct[(slug, "sec")] == 1)
    for col in ("lloc", *TESTED):
        lab = dict(QUALITY)[col]
        w(f"#### {lab}")
        w()
        w("| Model | n both | std | sec | diff | r (rank-biserial) | ties | p | Holm p |")
        w("|---|---|---|---|---|---|---|---|---|")
        recs, pr = [], []
        for slug, name in MODELS:
            both = both_idx[slug]
            xs = quality[(slug, "std")][col][both]
            ys = quality[(slug, "sec")][col][both]
            r = paired_wilcoxon(ys, xs)  # sec minus std
            recs.append((name, float(np.nanmean(xs)), float(np.nanmean(ys)), r))
            pr.append(r["p"])
        pa = holm(pr)
        for (name, ms, mc, r), a in zip(recs, pa):
            w(
                f"| {name} | {r['n']} | {ms:.3f} | {mc:.3f} | {r['mean_diff']:+.3f} | "
                f"{r['r_rb']:+.2f} | {r['n_zero']} | {fmt_p(r['p'])} | {fmt_p(a)} |"
            )
        w()

    # length decomposition
    w("### How much of the raw style change is explained by length")
    w()
    w(
        "On each model's jointly-correct set, write the mean raw flake8 count as "
        "the pooled rate times the mean logical length: mean(count) = "
        "(sum count / sum lloc) x mean(lloc). The counterfactual column is the "
        "security-focused mean raw count recomputed at the standard prompt's mean "
        "length, holding the security-focused rate fixed. `Length share` is the "
        "part of the observed change in the raw count that the length change "
        "accounts for."
    )
    w()
    w("| Model | n | raw std | raw sec | d raw | lloc std | lloc sec | d lloc | "
      "rate std | rate sec | counterfactual | length share (%) |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    decomp = []
    for slug, name in MODELS:
        both = both_idx[slug]
        Ms, Mc = meas[(slug, "std")], meas[(slug, "sec")]
        Qs, Qc = quality[(slug, "std")], quality[(slug, "sec")]
        ok = both & ~np.isnan(Qs["lloc"]) & ~np.isnan(Qc["lloc"])
        cs, cc_ = Ms["flake8_total"][ok], Mc["flake8_total"][ok]
        ls, lc = Qs["lloc"][ok], Qc["lloc"][ok]
        R_std, R_sec = float(cs.mean()), float(cc_.mean())
        L_std, L_sec = float(ls.mean()), float(lc.mean())
        r_std = 100 * cs.sum() / ls.sum()
        r_sec = 100 * cc_.sum() / lc.sum()
        cf = r_sec * L_std / 100.0  # sec rate at std length
        d_raw = R_sec - R_std
        length_part = R_sec - cf  # attributable to the length change
        share = 100 * length_part / d_raw if abs(d_raw) > 1e-12 else float("nan")
        decomp.append((name, int(ok.sum()), R_std, R_sec, d_raw, L_std, L_sec,
                       L_sec - L_std, r_std, r_sec, cf, share))
        w(
            f"| {name} | {int(ok.sum())} | {R_std:.2f} | {R_sec:.2f} | {d_raw:+.2f} | "
            f"{L_std:.1f} | {L_sec:.1f} | {L_sec-L_std:+.1f} | {r_std:.2f} | {r_sec:.2f} | "
            f"{cf:.2f} | {share:.0f} |"
        )
    w()

    # RQ2 security, descriptive
    w("### Bandit by severity on each model's jointly-correct set")
    w()
    w("| Model | n both | std HIGH | std MED | std LOW | std total | sec HIGH | sec MED | sec LOW | sec total |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for slug, name in MODELS:
        both = both_idx[slug]
        Ms, Mc = meas[(slug, "std")], meas[(slug, "sec")]
        w(
            f"| {name} | {int(both.sum())} | "
            f"{int(np.nansum(Ms['bandit_high'][both]))} | {int(np.nansum(Ms['bandit_medium'][both]))} | "
            f"{int(np.nansum(Ms['bandit_low'][both]))} | {int(np.nansum(Ms['bandit_total'][both]))} | "
            f"{int(np.nansum(Mc['bandit_high'][both]))} | {int(np.nansum(Mc['bandit_medium'][both]))} | "
            f"{int(np.nansum(Mc['bandit_low'][both]))} | {int(np.nansum(Mc['bandit_total'][both]))} |"
        )
    w()

    # ---------------- claim audit ----------------
    w("## Audit of the two published quality claims")
    w()
    order_style = sorted(
        MODELS,
        key=lambda mn: float(np.nanmean(quality[(mn[0], "std")]["style_per100_lloc"][common14])),
    )
    w(
        "**Claim 1 (RQ1): the Claude 4.x models write the least style-conformant code.** "
        f"Ranking on the {n14}-task set by flake8 violations per 100 logical lines, "
        "best to worst:"
    )
    w()
    w("| Rank | Model | Style /100 lloc | Excl. whitespace |")
    w("|---|---|---|---|")
    for i, (slug, name) in enumerate(order_style, 1):
        a = float(np.nanmean(quality[(slug, "std")]["style_per100_lloc"][common14]))
        b = float(np.nanmean(quality[(slug, "std")]["style_nonws_per100_lloc"][common14]))
        w(f"| {i} | {name} | {a:.2f} | {b:.2f} |")
    w()
    order_nonws = sorted(
        MODELS,
        key=lambda mn: float(np.nanmean(quality[(mn[0], "std")]["style_nonws_per100_lloc"][common14])),
    )
    w("Ranking excluding the whitespace-only codes, best to worst: "
      + ", ".join(n for _, n in order_nonws) + ".")
    w()

    w(
        "**Claim 2 (RQ2): the security-focused prompt lowers the style indicator "
        "for six of seven models.** Under the corrected indicator, the direction "
        "and significance per model:"
    )
    w()
    w("| Model | style std | style sec | diff (sec - std) | worse under sec? | p | Holm p |")
    w("|---|---|---|---|---|---|---|")
    recs, pr = [], []
    for slug, name in MODELS:
        both = both_idx[slug]
        xs = quality[(slug, "std")]["style_per100_lloc"][both]
        ys = quality[(slug, "sec")]["style_per100_lloc"][both]
        r = paired_wilcoxon(ys, xs)
        recs.append((name, float(np.nanmean(xs)), float(np.nanmean(ys)), r))
        pr.append(r["p"])
    pa = holm(pr)
    n_worse = 0
    n_worse_sig = 0
    for (name, ms, mc, r), a in zip(recs, pa):
        worse = "yes" if r["mean_diff"] > 0 else "no"
        n_worse += r["mean_diff"] > 0
        n_worse_sig += (r["mean_diff"] > 0) and a < 0.05
        w(
            f"| {name} | {ms:.2f} | {mc:.2f} | {r['mean_diff']:+.2f} | {worse} | "
            f"{fmt_p(r['p'])} | {fmt_p(a)} |"
        )
    w()
    w(
        f"Worse under the security-focused prompt: {n_worse} of {len(MODELS)} models; "
        f"significant after Holm: {n_worse_sig}."
    )
    w()

    # ---------------- RQ3 ----------------
    w("## RQ3. Correctness by category (standard prompt)")
    w()
    cat_of = {}
    cats_path = ROOT / "tasks" / "categories.json"
    if cats_path.exists():
        raw = json.loads(cats_path.read_text())
        if isinstance(raw, dict):
            for k, v in raw.items():
                if isinstance(v, str):
                    cat_of[k] = v
                elif isinstance(v, list):
                    for t in v:
                        cat_of[t] = k
    if cat_of:
        by_cat: dict[str, list[int]] = {}
        for i, t in enumerate(tasks):
            c = cat_of.get(t)
            if c:
                by_cat.setdefault(c, []).append(i)
        w("| Category | #Tasks | Mean (%) | Min model (%) | Max model (%) | Spread |")
        w("|---|---|---|---|---|---|")
        rows = []
        for cat, idx in by_cat.items():
            per = [100 * correct[(s, "std")][idx].mean() for s, _ in MODELS]
            rows.append((cat, len(idx), float(np.mean(per)), min(per), max(per)))
        for cat, n, mean, lo, hi in sorted(rows, key=lambda r: r[4] - r[3], reverse=True):
            w(f"| {cat} | {n} | {mean:.1f} | {lo:.1f} | {hi:.1f} | {hi-lo:.1f} |")
        w()
    else:
        w("Category map not found; category table skipped.")
        w()

    # The correlation between per-task correctness and hidden-test count is not
    # reported in the paper and is therefore not emitted here, so that this
    # report describes exactly the analyses the paper describes. It is reserved
    # for the extended version.

    out = OUT["md"]
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print(f"wrote {OUT['common14']}")
    print(f"wrote {OUT['jointly']}")
    print(f"wrote {OUT['pairwise']}")
    print(f"\n7-way jointly-correct set: {n_common7}/{n_tasks} tasks")
    print(f"14-way jointly-correct set: {n14}/{n_tasks} tasks")


if __name__ == "__main__":
    main()
