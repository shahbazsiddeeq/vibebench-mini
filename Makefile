# -------- VibeBench-Mini Makefile --------
PY ?= python3
VENV := .venv
ACT := . $(VENV)/bin/activate
METRICS ?= configs/metrics.v1.json

.PHONY: all venv install run analyze paper-snippets publish compare archive agents-baseline agents-clean ci-local format lint hooks clean help

all: run analyze

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(ACT); pip install --upgrade pip
	$(ACT); pip install -r requirements.txt

# Run the benchmark and export JSON/CSV/scorecard
# run:
# 	$(ACT); $(PY) runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv

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
# archive:
# 	$(ACT); $(PY) scripts/archive_run.py

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

# METRICS ?= configs/metrics.v1.json

run:
	$(ACT); $(PY) runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv --metrics $(METRICS)

ci-local: install
	$(ACT); METRICS=$(METRICS) $(PY) runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv --metrics $(METRICS)
	$(ACT); $(PY) scripts/analyze_results.py
runinfo:
	$(ACT); $(PY) scripts/runinfo.py
sweep:
	$(ACT); $(PY) scripts/sweep_metrics.py
archive:
	$(ACT); $(PY) scripts/archive_run.py --agent openai-default --agent copyref --agent naive --compress
# ---- JS track ----
run-js:
	@node runner/vibebench_runner_js.mjs

publish-js: run-js
	@mkdir -p dist
	@zip -rq dist/vibebench-js-results.zip results_js.json results_js.csv scorecard_js.md || true
	@echo "Wrote dist/vibebench-js-results.zip"
merge:
	@python scripts/merge_tracks.py

publish-all: run analyze run-js merge
	@mkdir -p dist
	@zip -rq dist/vibebench-all.zip results.json results.csv scorecard.md \
		results_js.json results_js.csv scorecard_js.md reports || true
	@echo "Wrote dist/vibebench-all.zip"

agents-js:
	@node scripts/agents_js/openai_agent.mjs

agents-js-summary:
	@python3 scripts/agents_js/summary.py

# agents-js-summary:
# 	@python3 - <<'PY'
# 	import csv, pathlib as p
# 	root = p.Path(".agent_runs/js/openai-default")
# 	f = root/"results.csv"
# 	if not f.exists():
# 		print("No JS agent results yet. Run: make agents-js"); raise SystemExit(0)
# 	rows = list(csv.DictReader(open(f, encoding="utf-8")))
# 	def tofloat(x): 
# 		try: return float(x)
# 		except: return float('nan')
# 	agg = sum(tofloat(r.get("aggregate_score","nan")) for r in rows)/max(1,len(rows))
# 	print(f"Tasks: {len(rows)}  Mean aggregate: {agg:.3f}")
# 	PY

agents-merge:
	@python3 scripts/agents_merge.py

# agents-publish: agents-merge
# 	@mkdir -p reports/agents
# 	@[ -f .agent_runs/openai-default/results.csv ] && cp .agent_runs/openai-default/results.csv reports/agents/py_results.csv || true
# 	@[ -f .agent_runs/js/openai-default/results.csv ] && cp .agent_runs/js/openai-default/results.csv reports/agents/js_results.csv || true
# 	@cp reports/agents_combined.md reports/ || true
# 	@echo "Agents artifacts prepared in reports/"

agents-costs:
	@python3 scripts/agents_cost_summary.py

agents-publish: agents-merge agents-costs
	@mkdir -p reports/agents
	@[ -f .agent_runs/openai-default/results.csv ] && cp .agent_runs/openai-default/results.csv reports/agents/py_results.csv || true
	@[ -f .agent_runs/js/openai-default/results.csv ] && cp .agent_runs/js/openai-default/results.csv reports/agents/js_results.csv || true
	@cp reports/agents_combined.md reports/ || true
	@cp reports/agents_costs.md reports/ || true
	@cp reports/agents_costs.csv reports/ || true
	@cp reports/agents_costs_by_track.csv reports/ || true
	@echo "Agents artifacts prepared in reports/"

release:
	@test -n "$(v)" || (echo "Usage: make release v=1.0.0" && exit 1)
	git tag -a v$(v) -m "VibeBench-Mini v$(v)"
	git push origin v$(v)
	@echo "Tag v$(v) pushed. GitHub Actions will build the release."

.PHONY: js-analyze js-all js-install js-run js-mutate js-publish

# js-mutate:
# 	@node runner/vibebench_runner_js.mjs

js-analyze:
	@python scripts/analyze_results.py

js-all: js-mutate js-analyze
	@echo "JS: results.json / results.csv / scorecard.md updated; see reports/"

# --- JS track ---

js-install:
	@npm ci || npm i

# Runs vitest/eslint/audit + complexity + mutation (per task)
js-run:
	@node runner/vibebench_runner_js.mjs

# Run a standalone Stryker session (optional)
js-mutate:
	@npx stryker run

# Bundle JS artifacts for sharing
js-publish: js-run
	@mkdir -p dist
	@zip -rq dist/vibebench-js-results.zip results_js.json results_js.csv scorecard_js.md || true
	@echo "Wrote dist/vibebench-js-results.zip"


