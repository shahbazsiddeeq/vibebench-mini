# VibeBench-Mini

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
[![Latest Results](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://shahbazsiddeeq.github.io/vibebench-mini/)
[![Version](https://img.shields.io/github/v/release/shahbazsiddeeq/vibebench-mini?color=blue)](https://github.com/shahbazsiddeeq/vibebench-mini/releases)


# ![CI](https://github.com/shahbazsiddeeq/vibebench-mini/actions/workflows/benchmark.yml/badge.svg)
# [![Latest Results](https://img.shields.io/badge/gh--pages-live-brightgreen)](https://shahbazsiddeeq.github.io/vibebench-mini/)
# [![Version](https://img.shields.io/badge/VibeBench--Mini-1.0.0-blue)](#)



All aggregates use configs/metrics.v1.json (weights in reports/metrics_used.md).
