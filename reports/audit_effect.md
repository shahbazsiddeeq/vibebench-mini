# What the audit changed

Every stored program for the 135 tasks present in both the pre-audit snapshot and the released benchmark, graded against each task's full suite before and after the audit-and-fix. No model output was regenerated.

Pre-audit assertions over these tasks: 814; after the audit: 1242.

| Configuration | Prompt | Pre-audit correct | Post-audit correct | Change (pp) | Accepted then rejected |
|---|---|---|---|---|---|
| GPT-4o-mini | std | 112 (83.0%) | 101 (74.8%) | -8.1 | 15 |
| GPT-4o-mini | sec | 109 (80.7%) | 96 (71.1%) | -9.6 | 17 |
| GPT-4o | std | 117 (86.7%) | 117 (86.7%) | +0.0 | 6 |
| GPT-4o | sec | 120 (88.9%) | 117 (86.7%) | -2.2 | 9 |
| GPT-5.6-sol | std | 128 (94.8%) | 133 (98.5%) | +3.7 | 2 |
| GPT-5.6-sol | sec | 128 (94.8%) | 132 (97.8%) | +3.0 | 3 |
| Claude Haiku 4.5 | std | 128 (94.8%) | 132 (97.8%) | +3.0 | 3 |
| Claude Haiku 4.5 | sec | 126 (93.3%) | 127 (94.1%) | +0.7 | 6 |
| Claude Sonnet 4.5 | std | 125 (92.6%) | 128 (94.8%) | +2.2 | 3 |
| Claude Sonnet 4.5 | sec | 127 (94.1%) | 130 (96.3%) | +2.2 | 3 |
| Claude Sonnet 5 | std | 127 (94.1%) | 133 (98.5%) | +4.4 | 1 |
| Claude Sonnet 5 | sec | 127 (94.1%) | 131 (97.0%) | +3.0 | 3 |
| Gemini 2.5 Flash | std | 123 (91.1%) | 124 (91.9%) | +0.7 | 6 |
| Gemini 2.5 Flash | sec | 122 (90.4%) | 122 (90.4%) | +0.0 | 6 |

Across all fourteen configurations, 83 of 1890 stored programs pass the pre-audit suite and fail the audited one. Aggregate correctness falls from 91.0% to 91.2%.
