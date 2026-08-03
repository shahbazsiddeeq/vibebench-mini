#!/usr/bin/env python3
"""Rebuild reports/r2_results_summary.csv from the repair audit.

The two figure scripts (gen_rev_ranking.py, gen_rev_barpanels.py) read this
file. It used to be written by hand, so it went stale whenever the audit was
re-run and the figures silently kept plotting superseded numbers. Deriving it
here keeps the figures tied to the same source the tables use, which is the
final_hidden_pass column of reports/r2_repair_audit.csv.

The percentage column is named correct_pct. It is final hidden-test correctness
under greedy decoding with at most one public-test-guided repair, which is not
the pass@k estimator, so it is not called pass@1.
"""

import collections
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "reports" / "r2_repair_audit.csv"
OUT = ROOT / "reports" / "r2_results_summary.csv"

SLUG = {
    "GPT-4o-mini": "gpt4omini",
    "GPT-4o": "gpt4o",
    "GPT-5.6-sol": "gpt56sol",
    "Claude Haiku 4.5": "haiku45",
    "Claude Sonnet 4.5": "sonnet45",
    "Claude Sonnet 5": "sonnet5",
    "Gemini 2.5 Flash": "gemini25",
}


def main() -> None:
    total = collections.Counter()
    passed = collections.Counter()
    for row in csv.DictReader(AUDIT.open()):
        config = f"{SLUG[row['model_label']]}-{row['prompt']}"
        total[config] += 1
        passed[config] += row["final_hidden_pass"] == "True"

    with OUT.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["config", "n_tasks", "n_pass", "correct_pct"])
        for config in sorted(total):
            n = total[config]
            k = passed[config]
            writer.writerow([config, n, k, f"{100 * k / n:.1f}"])

    print(f"wrote {OUT} ({len(total)} configurations)")


if __name__ == "__main__":
    main()
