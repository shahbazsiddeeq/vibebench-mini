#!/usr/bin/env bash
set -euo pipefail

# If the user passed commands, run them verbatim.
if [[ $# -gt 0 ]]; then
  exec "$@"
fi

# Default run: Python track ⇒ charts ⇒ bundle
echo "[vibebench] running default pipeline..."
python runner/vibebench_runner.py \
  --tasks tasks/python \
  --out results.json \
  --csv results.csv \
  --metrics configs/metrics.v1.json

python scripts/analyze_results.py || true
python scripts/paper_snippets.py || true

echo "[vibebench] done."