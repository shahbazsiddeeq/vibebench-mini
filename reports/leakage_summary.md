# Contamination and leakage audit

CodeAssay tasks: 185. Reference corpus: 1138 tasks (HumanEval 164 + MBPP 974).
Metric: maximum normalized character-level SequenceMatcher ratio against any reference task.
Candidate-overlap threshold: 0.70.

## Input digests (SHA-256)
- `HumanEval.jsonl`: `1d49078ba3e2b196b9344535bef34a43021f038fad9561d6ee7c53450609a6a2`
- `mbpp.jsonl`: `ccf64ceae9c5403bf50a044cb6d505bfd2a2963ee58338ba268fd65beab92a9f`

### Descriptions (title + description)
max 0.482 | mean 0.188 | median 0.107
- above 0.80: 0 tasks
- above 0.70: 0 tasks
- above 0.60: 0 tasks
- above 0.50: 0 tasks

### Descriptions (whole task.yaml, earlier method)
max 0.419 | mean 0.095 | median 0.075
- above 0.80: 0 tasks
- above 0.70: 0 tasks
- above 0.60: 0 tasks
- above 0.50: 0 tasks

### Reference solutions
max 0.640 | mean 0.123 | median 0.102
- above 0.80: 0 tasks
- above 0.70: 0 tasks
- above 0.60: 1 tasks
- above 0.50: 4 tasks

### Pairs above the 0.70 threshold: 0 (none)

### Five most similar descriptions
- task030: 0.482 vs mbpp/97
- task039: 0.465 vs mbpp/157
- task126: 0.438 vs mbpp/65
- task05: 0.437 vs mbpp/278
- task029: 0.437 vs mbpp/548

### Five most similar solutions
- task02: 0.640 vs mbpp/604
- task031: 0.536 vs mbpp/718
- task03: 0.518 vs mbpp/593
- task050: 0.506 vs mbpp/475
- task109: 0.466 vs mbpp/686

Per-task values: `reports/leakage_similarity.csv`.
