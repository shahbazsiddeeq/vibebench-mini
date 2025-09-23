# -------- VibeBench-Mini Makefile --------
PY ?= python3
VENV := .venv
ACT := . $(VENV)/bin/activate

.PHONY: all venv install run analyze paper-snippets publish compare archive agents-baseline agents-clean ci-local format lint hooks clean help

all: run analyze

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(ACT); pip install --upgrade pip
	$(ACT); pip install -r requirements.txt

# Run the benchmark and export JSON/CSV/scorecard
run:
	$(ACT); $(PY) runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv

# Generate charts + summary
analyze:
	$(ACT); $(PY) scripts/analyze_results.py

# Paper snippets (LaTeX/Markdown)
paper-snippets:
	$(ACT); $(PY) scripts/paper_snippets.py

# Zip bundle for sharing
publish: run analyze paper-snippets
	@mkdir -p dist
	@zip -rq dist/vibebench-results.zip results.json results.csv scorecard.md reports
	@echo "Wrote dist/vibebench-results.zip"

# Compare latest two archived runs
compare:
	$(ACT); $(PY) scripts/compare_runs.py

# Archive current results
archive:
	$(ACT); $(PY) scripts/archive_run.py

# Baseline agents harness
agents-baseline:
	$(ACT); $(PY) scripts/run_agents.py --config configs/agents.baseline.yaml

agents-clean:
	rm -rf .agent_runs

# Do what CI does locally
ci-local: install run analyze paper-snippets

# Code quality
format:
	$(ACT); black tasks runner scripts

lint:
	$(ACT); flake8 tasks runner scripts

hooks:
	$(ACT); pre-commit install
	$(ACT); pre-commit run -a

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache
	rm -rf reports dist history site .agent_runs
	rm -f results.json results.csv scorecard.md

help:
	@echo "Targets: install | run | analyze | paper-snippets | publish | compare | archive | agents-baseline | agents-clean | ci-local | format | lint | hooks | clean"

agents-openai:
	$(ACT); OPENAI_API_KEY=$${OPENAI_API_KEY} $(PY) scripts/run_agents.py --config configs/agents.openai.yaml

agents-compare:
	$(ACT); $(PY) scripts/run_agents.py --config configs/agents.compare.yaml

# agents-openai-cache-clear:
# 	rm -rf .agent_runs/openai-default/cache

# Deterministic, cheap baseline
agents-compare-deterministic:
	$(ACT); OPENAI_TEMPERATURE=0 OPENAI_MAX_OUTPUT_TOKENS=400 OPENAI_TOKEN_BUDGET=200000 $(PY) scripts/run_agents.py --config configs/agents.compare.yaml

# Clear OpenAI cache for a fresh run
agents-openai-cache-clear:
	rm -rf .agent_runs/openai-default/cache
agents-summary:
	$(ACT); $(PY) scripts/agents_summary.py

METRICS ?= configs/metrics.v1.json

run:
	$(ACT); $(PY) runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv --metrics $(METRICS)

ci-local: install
	$(ACT); METRICS=$(METRICS) $(PY) runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv --metrics $(METRICS)
	$(ACT); $(PY) scripts/analyze_results.py
runinfo:
	$(ACT); $(PY) scripts/runinfo.py
sweep:
	$(ACT); $(PY) scripts/sweep_metrics.py