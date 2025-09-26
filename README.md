# VibeBench-Mini

![CI](https://github.com/shahbazsiddeeq/vibebench-mini/actions/workflows/benchmark.yml/badge.svg)
[![Latest Results](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://shahbazsiddeeq.github.io/vibebench-mini/)
[![Version](https://img.shields.io/badge/VibeBench--Mini-1.0.0-blue)](#)

A tiny, **multi-metric** benchmark for AI-assisted coding (Python first).  
It produces a scorecard covering **correctness**, **complexity**, **lint**, **security**, and **dependency vulnerabilities**.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python runner/vibebench_runner.py --tasks tasks/python --out results.json
```

### Outputs

- `results.json` — machine-readable scores  
- `scorecard.md` — human-friendly table  

## Metrics v1.0 (frozen)

- **Correctness** = passed / total tests (pytest JUnit).  
- **Complexity**: avg cyclomatic complexity → 1.0 if ≤5, 0.0 if ≥15 (linear in between).  
- **Lint**: flake8 errors → 1.0 if 0, 0.0 if ≥20.  
- **Security**: Bandit findings → 1.0 if 0, 0.0 if ≥20.  
- **Dependency vulns**: pip-audit count → 1.0 if 0, 0.0 if ≥10.  
- **Aggregate**: mean of available subscores.  


### Run via Docker (no local Python/Node setup)

```bash
# default (Python track + charts)
docker run --rm -it \
  -v "$PWD":/work -w /work \
  ghcr.io/shahbazsiddeeq/vibebench-mini:latest

# JS track
docker run --rm -it \
  -v "$PWD":/work -w /work \
  ghcr.io/shahbazsiddeeq/vibebench-mini:latest \
  node runner/vibebench_runner_js.mjs

# With OpenAI agents
docker run --rm -it \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -v "$PWD":/work -w /work \
  ghcr.io/shahbazsiddeeq/vibebench-mini:latest \
  python scripts/run_agents.py --config configs/agents.openai.yaml
```

## Quick sanity check (now)

1) Rebuild locally with the entrypoint:

```bash
docker build -t vibebench-mini:local .
docker run --rm -it -v "$PWD":/work -w /work vibebench-mini:local
```
2) If it runs, push a tag to trigger CI image tagging:

```bash
git tag v1.0.0
git push origin v1.0.0
```

### Paper artifacts

Make LaTeX/Markdown snippets:

```bash
make paper-snippets
```

---


All aggregates use `configs/metrics.v1.json` (weights in `reports/metrics_used.md`).
