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

## Metrics v1.0 (frozen)
- **Correctness** = passed / total tests (pytest JUnit).
- **Complexity**: avg cyclomatic complexity → 1.0 if ≤5, 0.0 if ≥15 (linear in between).
- **Lint**: flake8 errors → 1.0 if 0, 0.0 if ≥20.
- **Security**: Bandit findings → 1.0 if 0, 0.0 if ≥20.
- **Dependency vulns**: pip-audit count → 1.0 if 0, 0.0 if ≥10.
- **Aggregate**: mean of available subscores.

### Paper artifacts
- Make LaTeX/Markdown snippets:
  ```bash
  make paper-snippets


![CI](https://github.com/shahbazsiddeeq/vibebench-mini/actions/workflows/benchmark.yml/badge.svg)
