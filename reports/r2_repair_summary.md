# Repair pipeline reported in parts (r2 run)

Produced by `scripts/r2_repair_audit.py`. Every first attempt and every final solution was graded from scratch against the public suite and the hidden suite, in an isolated directory holding the task source and exactly one suite. The repair decision fields come from `events.jsonl`, which the run wrote at the moment each decision was taken.

## Column meanings

* Attempt 1 public pass: the first generated program passed the public tests. These tasks are not eligible for repair.
* Repair eligible: the first program failed the public tests, which is the condition the pipeline uses to fire the repair.
* Repairs attempted: an eligible task for which a second API call was issued. Skipped tasks are eligible tasks with no second call, and the reason is given in the next table.
* Repairs passing public: repaired programs that passed the public tests afterwards.
* Initial hidden pass: the first attempt graded on the hidden tests. Final hidden pass: the scored solution graded on the hidden tests.

## Repair pipeline per configuration

| Configuration | Prompt | Tasks graded | Status | Attempt 1 available | Attempt 1 public pass | Repair eligible | Repairs attempted | Repairs skipped | Repairs passing public | Initial hidden pass | Final hidden pass | Hidden fail to pass | Hidden pass to fail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 Flash | sec | 185 | complete | 185 | 174 (94.1%) | 11 | 11 | 0 | 8 | 164 (88.6%) | 169 (91.4%) | 5 | 0 |
| Gemini 2.5 Flash | std | 185 | complete | 185 | 176 (95.1%) | 9 | 9 | 0 | 7 | 169 (91.4%) | 169 (91.4%) | 1 | 1 |
| GPT-4o | sec | 185 | complete | 185 | 163 (88.1%) | 22 | 22 | 0 | 11 | 161 (87.0%) | 166 (89.7%) | 5 | 0 |
| GPT-4o | std | 185 | complete | 185 | 165 (89.2%) | 20 | 20 | 0 | 8 | 154 (83.2%) | 161 (87.0%) | 7 | 0 |
| GPT-4o-mini | sec | 185 | complete | 185 | 147 (79.5%) | 38 | 38 | 0 | 7 | 137 (74.1%) | 139 (75.1%) | 3 | 1 |
| GPT-4o-mini | std | 185 | complete | 185 | 150 (81.1%) | 35 | 35 | 0 | 9 | 142 (76.8%) | 143 (77.3%) | 4 | 3 |
| GPT-5.6-sol | sec | 185 | complete | 185 | 185 (100.0%) | 0 | 0 | 0 | 0 | 182 (98.4%) | 182 (98.4%) | 0 | 0 |
| GPT-5.6-sol | std | 185 | complete | 185 | 184 (99.5%) | 1 | 1 | 0 | 1 | 183 (98.9%) | 183 (98.9%) | 0 | 0 |
| Claude Haiku 4.5 | sec | 185 | complete | 185 | 180 (97.3%) | 5 | 5 | 0 | 4 | 172 (93.0%) | 175 (94.6%) | 3 | 0 |
| Claude Haiku 4.5 | std | 185 | complete | 185 | 181 (97.8%) | 4 | 4 | 0 | 3 | 177 (95.7%) | 179 (96.8%) | 2 | 0 |
| Claude Sonnet 4.5 | sec | 185 | complete | 185 | 181 (97.8%) | 4 | 4 | 0 | 3 | 174 (94.1%) | 177 (95.7%) | 3 | 0 |
| Claude Sonnet 4.5 | std | 185 | complete | 185 | 181 (97.8%) | 4 | 4 | 0 | 4 | 173 (93.5%) | 176 (95.1%) | 3 | 0 |
| Claude Sonnet 5 | sec | 185 | complete | 185 | 183 (98.9%) | 2 | 2 | 0 | 2 | 181 (97.8%) | 181 (97.8%) | 0 | 0 |
| Claude Sonnet 5 | std | 185 | complete | 185 | 184 (99.5%) | 1 | 1 | 0 | 1 | 182 (98.4%) | 183 (98.9%) | 1 | 0 |

The two attempt 1 percentages are shares of the tasks that have a stored first attempt. The final hidden percentage is a share of the tasks that have a stored final solution. Both denominators equal 185 only when the row is marked complete.

## Reasons a repair was not attempted

`passed` means the first attempt already passed the public tests. `no_repair_flag` means the repair step was disabled for that call. `over_budget` means the token budget was exhausted before the repair. `missing` means no repair decision was logged for the task.

| Configuration | Prompt | passed | no_repair_flag | over_budget | missing | Eligible but skipped |
|---|---|---|---|---|---|---|
| Gemini 2.5 Flash | sec | 174 | 0 | 0 | 0 | 0 |
| Gemini 2.5 Flash | std | 176 | 0 | 0 | 0 | 0 |
| GPT-4o | sec | 163 | 0 | 0 | 0 | 0 |
| GPT-4o | std | 165 | 0 | 0 | 0 | 0 |
| GPT-4o-mini | sec | 147 | 0 | 0 | 0 | 0 |
| GPT-4o-mini | std | 150 | 0 | 0 | 0 | 0 |
| GPT-5.6-sol | sec | 185 | 0 | 0 | 0 | 0 |
| GPT-5.6-sol | std | 184 | 0 | 0 | 0 | 0 |
| Claude Haiku 4.5 | sec | 180 | 0 | 0 | 0 | 0 |
| Claude Haiku 4.5 | std | 181 | 0 | 0 | 0 | 0 |
| Claude Sonnet 4.5 | sec | 181 | 0 | 0 | 0 | 0 |
| Claude Sonnet 4.5 | std | 181 | 0 | 0 | 0 | 0 |
| Claude Sonnet 5 | sec | 183 | 0 | 0 | 0 | 0 |
| Claude Sonnet 5 | std | 184 | 0 | 0 | 0 | 0 |

## Data completeness and consistency

| Configuration | Prompt | Tasks graded | Missing attempt 1 | Missing final | No program | Budget skips | API errors | Log and regrade disagree | Runner results disagree |
|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 Flash | sec | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Gemini 2.5 Flash | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GPT-4o | sec | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GPT-4o | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GPT-4o-mini | sec | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GPT-4o-mini | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GPT-5.6-sol | sec | 185 | 0 | 0 | 2 | 0 | 2 | 0 | 0 |
| GPT-5.6-sol | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claude Haiku 4.5 | sec | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claude Haiku 4.5 | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claude Sonnet 4.5 | sec | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claude Sonnet 4.5 | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claude Sonnet 5 | sec | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claude Sonnet 5 | std | 185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The last column is empty of meaning until the runner has written `results.csv` for a configuration. Rows with no recorded value are not counted as disagreements.

