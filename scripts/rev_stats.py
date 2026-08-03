#!/usr/bin/env python3
"""PROFES-revision statistics on the hidden-test rerun (.agent_runs/*/results.csv).

RQ1: compare the 7 models (standard prompt) on per-task correctness (hidden pass-rate)
     -> pass@1 + bootstrap 95% CI, Friedman, pairwise Wilcoxon+Holm-Bonferroni, Cliff's d.
RQ2: security-prompt effect per model (paired std vs sec) -> pass@1 delta, Wilcoxon, Cliff's d.
RQ3: correctness by category; Spearman(task difficulty vs test count / complexity).
Quality among all-hidden-pass solutions (strict gate): complexity/style/security, N-per-cell.
Writes reports/rev_stats_summary.md.
"""
import csv
import json
import glob
import os
import random
import statistics as st
from itertools import combinations

from scipy.stats import friedmanchisquare, wilcoxon, spearmanr

random.seed(12345)
MODELS = ["gpt4omini", "gpt4o", "gpt56sol", "haiku45", "sonnet45", "sonnet5", "gemini25"]
LABEL = {"gpt4omini": "GPT-4o-mini", "gpt4o": "GPT-4o", "gpt56sol": "GPT-5.6-sol",
         "haiku45": "Claude Haiku 4.5", "sonnet45": "Claude Sonnet 4.5",
         "sonnet5": "Claude Sonnet 5", "gemini25": "Gemini 2.5 Flash"}
CATS = json.load(open("tasks/categories.json"))


def load(name):
    d = {}
    for r in csv.DictReader(open(f".agent_runs/{name}/results.csv")):
        if r["id"] == "__aggregate__":
            continue
        def f(k):
            try:
                return float(r[k])
            except (KeyError, ValueError, TypeError):
                return None
        d[r["id"]] = {"corr": f("correctness"), "cplx": f("complexity_score"),
                      "style": f("lint_score"), "sec": f("security_score"),
                      "tests": f("tests_total")}
    return d


DATA = {f"{m}-{v}": load(f"{m}-{v}") for m in MODELS for v in ("std", "sec")}
TASKS = sorted(set.intersection(*(set(d) for d in DATA.values())))


def corr_vec(name):
    return [DATA[name][t]["corr"] or 0.0 for t in TASKS]


def passk(name):
    return sum(1 for t in TASKS if (DATA[name][t]["corr"] or 0) == 1.0)


def boot_ci(vec, n=2000):
    means = []
    for _ in range(n):
        s = [vec[random.randrange(len(vec))] for _ in range(len(vec))]
        means.append(sum(s) / len(s))
    means.sort()
    return means[int(0.025 * n)], means[int(0.975 * n)]


def cliffs_delta(a, b):
    gt = sum(1 for x in a for y in b if x > y)
    lt = sum(1 for x in a for y in b if x < y)
    return (gt - lt) / (len(a) * len(b))


def dmag(d):
    a = abs(d)
    return "negligible" if a < .147 else "small" if a < .33 else "medium" if a < .474 else "large"


out = ["# CodeAssay revision statistics (hidden-test rerun)\n",
       f"Tasks: {len(TASKS)}. Models: 7. Prompts: standard, secure.\n"]

# ---- RQ1: standard-prompt model comparison ----
out.append("## RQ1 - model comparison (standard prompt), pass@1 on hidden tests\n")
out.append("| Model | pass@1 | % | bootstrap 95% CI |\n|---|---|---|---|")
std_pass = {}
for m in MODELS:
    name = f"{m}-std"
    p = passk(name)
    lo, hi = boot_ci([1.0 if (DATA[name][t]["corr"] or 0) == 1.0 else 0.0 for t in TASKS])
    std_pass[m] = p
    out.append(f"| {LABEL[m]} | {p}/{len(TASKS)} | {100*p/len(TASKS):.1f} | [{100*lo:.1f}, {100*hi:.1f}] |")
vecs = [corr_vec(f"{m}-std") for m in MODELS]
chi, pv = friedmanchisquare(*vecs)
out.append(f"\nFriedman across 7 std models (per-task hidden pass-rate): chi2={chi:.2f}, p={pv:.2e}\n")
out.append("Pairwise Wilcoxon signed-rank (zero_method=pratt), Holm-Bonferroni corrected; Cliff's d:\n")
out.append("| pair | p_raw | p_holm | Cliff d | mag |\n|---|---|---|---|---|")
pairs = list(combinations(range(len(MODELS)), 2))
raw = []
for i, j in pairs:
    a, b = vecs[i], vecs[j]
    if a == b:
        raw.append(1.0)
        continue
    try:
        _, p = wilcoxon(a, b, zero_method="pratt")
    except ValueError:
        p = 1.0
    raw.append(p)
order = sorted(range(len(pairs)), key=lambda k: raw[k])
holm = [None] * len(pairs)
mtests = len(pairs)
for rank, k in enumerate(order):
    holm[k] = min(1.0, raw[k] * (mtests - rank))
for k in range(1, len(order)):
    holm[order[k]] = max(holm[order[k]], holm[order[k-1]])
for k, (i, j) in enumerate(pairs):
    d = cliffs_delta(vecs[i], vecs[j])
    out.append(f"| {LABEL[MODELS[i]]} vs {LABEL[MODELS[j]]} | {raw[k]:.3g} | {holm[k]:.3g} | {d:+.3f} | {dmag(d)} |")

# ---- RQ2: security-prompt effect ----
out.append("\n## RQ2 - security-prompt effect (paired std vs secure, per model)\n")
out.append("| Model | pass@1 std | pass@1 sec | delta pts | Wilcoxon p | Cliff d | mag |\n|---|---|---|---|---|---|---|")
for m in MODELS:
    s, c = corr_vec(f"{m}-std"), corr_vec(f"{m}-sec")
    ps, pc = passk(f"{m}-std"), passk(f"{m}-sec")
    try:
        _, p = wilcoxon(s, c, zero_method="pratt") if s != c else (0, 1.0)
    except ValueError:
        p = 1.0
    d = cliffs_delta(c, s)  # positive = secure better
    out.append(f"| {LABEL[m]} | {100*ps/len(TASKS):.1f} | {100*pc/len(TASKS):.1f} | "
               f"{100*(pc-ps)/len(TASKS):+.1f} | {p:.3g} | {d:+.3f} | {dmag(d)} |")

# ---- RQ3: category + difficulty ----
out.append("\n## RQ3 - variation across categories (standard prompt)\n")
cat_ids = {}
for t in TASKS:
    cat_ids.setdefault(CATS.get(t, "?"), []).append(t)
out.append("| Category | #tasks | mean pass@1 across models | min model | max model | spread |\n|---|---|---|---|---|---|")
for cat, ids in sorted(cat_ids.items()):
    permodel = []
    for m in MODELS:
        name = f"{m}-std"
        permodel.append(sum(1 for t in ids if (DATA[name][t]["corr"] or 0) == 1.0) / len(ids))
    out.append(f"| {cat} | {len(ids)} | {100*st.mean(permodel):.1f} | {100*min(permodel):.1f} | "
               f"{100*max(permodel):.1f} | {100*(max(permodel)-min(permodel)):.1f} |")
# task difficulty = mean correctness across std models; correlate w/ test count & complexity
diff = {t: st.mean([DATA[f"{m}-std"][t]["corr"] or 0 for m in MODELS]) for t in TASKS}
tc = [DATA["gpt4o-std"][t]["tests"] or 0 for t in TASKS]
rho_tc, p_tc = spearmanr([diff[t] for t in TASKS], tc)
out.append(f"\nSpearman(task mean-correctness, hidden test count): rho={rho_tc:.3f}, p={p_tc:.3g}\n")

# ---- Quality among passers ----
out.append("\n## Quality indicators among all-hidden-pass solutions (strict gate); N = #passers\n")
out.append("| Config | N pass | complexity | style | security |\n|---|---|---|---|---|")
for m in MODELS:
    for v in ("std", "sec"):
        name = f"{m}-{v}"
        passers = [t for t in TASKS if (DATA[name][t]["corr"] or 0) == 1.0]
        def mq(k):
            xs = [DATA[name][t][k] for t in passers if DATA[name][t][k] is not None]
            return round(st.mean(xs), 3) if xs else None
        out.append(f"| {LABEL[m]} ({v}) | {len(passers)} | {mq('cplx')} | {mq('style')} | {mq('sec')} |")

os.makedirs("reports", exist_ok=True)
open("reports/rev_stats_summary.md", "w").write("\n".join(out))
print("\n".join(out))
print("\nwrote reports/rev_stats_summary.md")
