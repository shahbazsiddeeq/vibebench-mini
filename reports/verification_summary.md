# Verification re-grade and repair accounting

Produced by `scripts/verify_and_repair_audit.py`. Every stored solution was re-graded from scratch against the final split, in an isolated directory containing the task source and exactly one test suite.

## Reproduction of the reported correctness values

| Configuration | Prompt | Solutions | Reproduced | Mismatches | Hidden pass (recomputed) | Reported |
|---|---|---|---|---|---|---|
| GPT-4o-mini | std | 185 | 185 | 0 | 77.3% | 77.3% |
| GPT-4o-mini | sec | 185 | 185 | 0 | 75.1% | 75.1% |
| GPT-4o | std | 185 | 185 | 0 | 87.0% | 87.0% |
| GPT-4o | sec | 185 | 185 | 0 | 89.7% | 89.7% |
| GPT-5.6-sol | std | 185 | 185 | 0 | 98.9% | 98.9% |
| GPT-5.6-sol | sec | 185 | 185 | 0 | 98.4% | 98.4% |
| Claude Haiku 4.5 | std | 185 | 185 | 0 | 96.8% | 96.8% |
| Claude Haiku 4.5 | sec | 185 | 185 | 0 | 94.6% | 94.6% |
| Claude Sonnet 4.5 | std | 185 | 185 | 0 | 95.1% | 95.1% |
| Claude Sonnet 4.5 | sec | 185 | 185 | 0 | 95.7% | 95.7% |
| Claude Sonnet 5 | std | 185 | 185 | 0 | 98.9% | 98.9% |
| Claude Sonnet 5 | sec | 185 | 185 | 0 | 97.8% | 97.8% |
| Gemini 2.5 Flash | std | 185 | 185 | 0 | 91.4% | 91.4% |
| Gemini 2.5 Flash | sec | 185 | 185 | 0 | 91.4% | 91.4% |

Total solutions re-graded: 2590. Total disagreements with the recorded results: 0.

## Repair accounting

The repair step fires when the first attempt fails the public tests. The identity below needs a ledger covering a single pass over the task set and a program for every task; it does not hold when a task returned no program, when the token budget was exhausted, or when a cached solution was reused. Configurations where any of these occurred are reported as not recoverable. For a configuration with a single clean run, the number of repair calls is the request count minus one call per task. Solutions whose final stored version still fails the public tests are repairs that did not recover. The hidden-test correctness of the first attempt is not recoverable, because the cache retains only the final solution.

| Configuration | Prompt | Requests | Passed first attempt | Repairs attempted | Repairs recovered public | Final fails public | Final hidden pass |
|---|---|---|---|---|---|---|---|
| GPT-4o-mini | std | 220 | 150 | 35 | 9 | 26 | 77.3% |
| GPT-4o-mini | sec | 223 | 147 | 38 | 7 | 31 | 75.1% |
| GPT-4o | std | 205 | 165 | 20 | 8 | 12 | 87.0% |
| GPT-4o | sec | 207 | 163 | 22 | 11 | 11 | 89.7% |
| GPT-5.6-sol | std | 186 | not recoverable | not recoverable | not recoverable | 0 | 98.9% |
| GPT-5.6-sol | sec | 185 | not recoverable | not recoverable | not recoverable | 0 | 98.4% |
| Claude Haiku 4.5 | std | 189 | 181 | 4 | 3 | 1 | 96.8% |
| Claude Haiku 4.5 | sec | 190 | 180 | 5 | 4 | 1 | 94.6% |
| Claude Sonnet 4.5 | std | 189 | 181 | 4 | 4 | 0 | 95.1% |
| Claude Sonnet 4.5 | sec | 189 | 181 | 4 | 3 | 1 | 95.7% |
| Claude Sonnet 5 | std | 186 | not recoverable | not recoverable | not recoverable | 0 | 98.9% |
| Claude Sonnet 5 | sec | 187 | not recoverable | not recoverable | not recoverable | 0 | 97.8% |
| Gemini 2.5 Flash | std | 194 | 176 | 9 | 7 | 2 | 91.4% |
| Gemini 2.5 Flash | sec | 196 | 174 | 11 | 8 | 3 | 91.4% |

Configurations marked not recoverable are the four frontier runs, which were relaunched after two mid-run corrections, so their ledgers no longer correspond to a single pass over the task set.

