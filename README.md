# VibeBench-Mini (Starter)

A tiny, **multi-metric** benchmark for AI-assisted coding (Python first).
It produces a scorecard covering **correctness**, **complexity**, **lint**, **security**, and **dependency vulnerabilities**.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python runner/vibebench_runner.py --tasks tasks/python --out results.json
Outputs:

results.json — machine-readable scores

scorecard.md — human-friendly table
