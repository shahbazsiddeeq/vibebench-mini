# Changelog

## [2.0.0] - 2026-08-03
### Changed
- The project is renamed from VibeBench (VibeBench-Mini) to CodeAssay. Names in
  the Makefile, Dockerfile, CI workflows, scripts, runner and packaging metadata
  now use CodeAssay/codeassay.
- Runner files moved: `runner/vibebench_runner.py` -> `runner/codeassay_runner.py`
  and `runner/vibebench_runner_js.mjs` -> `runner/codeassay_runner_js.mjs`. All
  call sites were updated.
- Docker entrypoint renamed from `vibebench` to `codeassay`. A symlink
  `/usr/local/bin/vibebench` -> `/usr/local/bin/codeassay` is installed so
  existing invocations keep working.
- Environment variable `VIBEBENCH_RUNNER_LIMIT` renamed to
  `CODEASSAY_RUNNER_LIMIT`. The old name is still read as a fallback; the new
  name takes precedence when both are set.
- The GitHub repository is renamed from `vibebench` to `CodeAssay` and moved
  from a personal account to the `Code-Assay` organization, so the canonical URL
  is now `https://github.com/Code-Assay/CodeAssay`. `CITATION.cff` and
  `.zenodo.json` record it. GitHub redirects the earlier URLs, including `git`
  remotes, but a redirect lapses if its old name is later reused, so prefer the
  current URL in new citations. The previous `CITATION.cff` value
  (`.../vibebench-mini`) never matched any remote and was wrong independently of
  these moves.

### Unchanged
- The metrics configuration ids `VibeBench-v1.0`, `VibeBench-v1-dev` and
  `VibeBench-v1-secure` keep their old values. The runner stamps them verbatim
  into `aggregate.metrics_id` in already-published `results.json` files, so
  renaming them would break the correspondence between a published result and
  the configuration that produced it. They are data values, not product names.

## [1.0.0] - 2025-09-25
### Added
- Python track (17 tasks) with multi-metric runner (correctness, complexity, lint, security, deps, mutation).
- JS track (5 tasks) with Vitest/ESLint runner.
- Agents baseline (naive, copyref, OpenAI) + compare/summary reports.
- Cost & usage summary (CSV/MD) and GitHub Pages publishing.

### Fixed
- CI stability, pre-commit config, metrics export (JSON/CSV/MD/plots).
