#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "runner" / "vibebench_runner.py"
CONFIGS = [
    "configs/metrics.v1.json",
    "configs/metrics.v1.dev.json",
    "configs/metrics.v1.secure.json",
]
OUTDIR = ROOT / "reports" / "sweeps"
OUTDIR.mkdir(parents=True, exist_ok=True)

rows = []
for cfg in CONFIGS:
    tag = Path(cfg).stem
    j = OUTDIR / f"results__{tag}.json"
    c = OUTDIR / f"results__{tag}.csv"
    subprocess.check_call(
        [
            "python",
            str(RUNNER),
            "--tasks",
            "tasks/python",
            "--out",
            str(j),
            "--csv",
            str(c),
            "--metrics",
            cfg,
        ]
    )
    data = json.loads(j.read_text(encoding="utf-8"))
    agg = data["aggregate"]
    rows.append((tag, agg.get("metrics_id"), agg["mean_score"], agg["metrics_weights"]))

md = [
    "## Metrics Sweep (Python tasks)",
    "",
    "| tag | metrics_id | mean_agg | weights |",
    "|---|---|---:|---|",
]
for tag, mid, mean, w in rows:
    md.append(f"| {tag} | `{mid}` | **{mean:.3f}** | `{w}` |")
(OUTDIR / "metrics_sweep.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("Wrote", OUTDIR / "metrics_sweep.md")
