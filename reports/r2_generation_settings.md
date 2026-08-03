# Generation settings actually used (r2 run)

Produced by `scripts/r2_generation_settings.py`. The settings columns come from each run's `runinfo.json`, which the agent writes before the first call. The accounting columns come from each run's `events.jsonl`, which records one object per API call. The temperature column reports the value the client sent. A model that rejects the parameter is shown as provider default, and no temperature was sent for those runs.

## Settings

| Configuration | Prompt | Model id | Provider | Endpoint | Temperature sent | Max output tokens | Token budget | Repair enabled | SDK | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 Flash | sec | `google/gemini-2.5-flash` | openrouter | `chat.completions.create` | 0.0 | 16384 | 10000000 | True | openai (OpenRouter-compatible client) 1.107.3 | complete |
| Gemini 2.5 Flash | std | `google/gemini-2.5-flash` | openrouter | `chat.completions.create` | 0.0 | 16384 | 10000000 | True | openai (OpenRouter-compatible client) 1.107.3 | complete |
| GPT-4o | sec | `gpt-4o` | openai | `responses.create` | 0.0 | 16384 | 10000000 | True | openai 1.107.3 | complete |
| GPT-4o | std | `gpt-4o` | openai | `responses.create` | 0.0 | 16384 | 10000000 | True | openai 1.107.3 | complete |
| GPT-4o-mini | sec | `gpt-4o-mini` | openai | `responses.create` | 0.0 | 16384 | 10000000 | True | openai 1.107.3 | complete |
| GPT-4o-mini | std | `gpt-4o-mini` | openai | `responses.create` | 0.0 | 16384 | 10000000 | True | openai 1.107.3 | complete |
| GPT-5.6-sol | sec | `gpt-5.6-sol` | openai | `responses.create` | provider default | 16384 | 10000000 | True | openai 1.107.3 | complete |
| GPT-5.6-sol | std | `gpt-5.6-sol` | openai | `responses.create` | provider default | 16384 | 10000000 | True | openai 1.107.3 | complete |
| Claude Haiku 4.5 | sec | `claude-haiku-4-5-20251001` | anthropic | `messages.create` | 0.0 | 16384 | 10000000 | True | anthropic 0.101.0 | complete |
| Claude Haiku 4.5 | std | `claude-haiku-4-5-20251001` | anthropic | `messages.create` | 0.0 | 16384 | 10000000 | True | anthropic 0.101.0 | complete |
| Claude Sonnet 4.5 | sec | `claude-sonnet-4-5-20250929` | anthropic | `messages.create` | 0.0 | 16384 | 10000000 | True | anthropic 0.101.0 | complete |
| Claude Sonnet 4.5 | std | `claude-sonnet-4-5-20250929` | anthropic | `messages.create` | 0.0 | 16384 | 10000000 | True | anthropic 0.101.0 | complete |
| Claude Sonnet 5 | sec | `claude-sonnet-5` | anthropic | `messages.create` | provider default | 16384 | 10000000 | True | anthropic 0.101.0 | complete |
| Claude Sonnet 5 | std | `claude-sonnet-5` | anthropic | `messages.create` | provider default | 16384 | 10000000 | True | anthropic 0.101.0 | complete |

## API accounting

| Configuration | Prompt | Tasks seen | API calls | First attempts | Repair calls | Errors | Truncated | Prompt tokens | Completion tokens | Total tokens | Reasoning tokens | Cached tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 Flash | sec | 185 | 196 | 185 | 11 | 0 | 0 | 117288 | 144833 | 262121 | 0 | 0 |
| Gemini 2.5 Flash | std | 185 | 194 | 185 | 9 | 0 | 0 | 108411 | 89350 | 197761 | 0 | 0 |
| GPT-4o | sec | 185 | 207 | 185 | 22 | 0 | 0 | 114132 | 49485 | 163617 | 0 | 0 |
| GPT-4o | std | 185 | 205 | 185 | 20 | 0 | 0 | 103571 | 42932 | 146503 | 0 | 0 |
| GPT-4o-mini | sec | 185 | 223 | 185 | 38 | 0 | 0 | 127230 | 59076 | 186306 | 0 | 0 |
| GPT-4o-mini | std | 185 | 220 | 185 | 35 | 0 | 0 | 117161 | 48925 | 166086 | 0 | 0 |
| GPT-5.6-sol | sec | 185 | 187 | 187 | 0 | 2 | 0 | 94607 | 183198 | 277805 | 113011 | 0 |
| GPT-5.6-sol | std | 185 | 186 | 185 | 1 | 0 | 0 | 89128 | 105426 | 194554 | 57640 | 0 |
| Claude Haiku 4.5 | sec | 185 | 190 | 185 | 5 | 0 | 0 | 116435 | 121569 | 238004 | 0 | 0 |
| Claude Haiku 4.5 | std | 185 | 189 | 185 | 4 | 0 | 0 | 107807 | 94705 | 202512 | 0 | 0 |
| Claude Sonnet 4.5 | sec | 185 | 189 | 185 | 4 | 0 | 0 | 115179 | 122577 | 237756 | 0 | 0 |
| Claude Sonnet 4.5 | std | 185 | 189 | 185 | 4 | 0 | 0 | 107640 | 113139 | 220779 | 0 | 0 |
| Claude Sonnet 5 | sec | 185 | 187 | 185 | 2 | 0 | 0 | 147021 | 231252 | 378273 | 0 | 0 |
| Claude Sonnet 5 | std | 185 | 186 | 185 | 1 | 0 | 0 | 134768 | 84292 | 219060 | 0 | 0 |

First attempts and repair calls are counts of API calls carrying attempt 1 and attempt 2. A retried call adds to the count, so these numbers can exceed the number of tasks.

## Finish reasons and truncation

| Configuration | Prompt | Finish reason distribution | Truncated calls | Incomplete reasons | Error types |
|---|---|---|---|---|---|
| Gemini 2.5 Flash | sec | stop 196 | 0 | none | none |
| Gemini 2.5 Flash | std | stop 194 | 0 | none | none |
| GPT-4o | sec | completed 207 | 0 | none | none |
| GPT-4o | std | completed 205 | 0 | none | none |
| GPT-4o-mini | sec | completed 223 | 0 | none | none |
| GPT-4o-mini | std | completed 220 | 0 | none | none |
| GPT-5.6-sol | sec | completed 185; None 2 | 0 | none | APITimeoutError 2 |
| GPT-5.6-sol | std | completed 186 | 0 | none | none |
| Claude Haiku 4.5 | sec | end_turn 190 | 0 | none | none |
| Claude Haiku 4.5 | std | end_turn 189 | 0 | none | none |
| Claude Sonnet 4.5 | sec | end_turn 189 | 0 | none | none |
| Claude Sonnet 4.5 | std | end_turn 189 | 0 | none | none |
| Claude Sonnet 5 | sec | end_turn 187 | 0 | none | none |
| Claude Sonnet 5 | std | end_turn 186 | 0 | none | none |

A truncated call is one the provider stopped at the output cap. The finish reason names differ by provider. The OpenAI Responses API reports `completed`, the Anthropic Messages API reports `end_turn`, and the OpenRouter chat completions API reports `stop`. All three mean the model finished on its own.

## Cost ledgers

| Configuration | Prompt | Requests | Input tokens | Output tokens |
|---|---|---|---|---|
| Gemini 2.5 Flash | sec | 196 | 117288 | 144833 |
| Gemini 2.5 Flash | std | 194 | 108411 | 89350 |
| GPT-4o | sec | 207 | 114132 | 49485 |
| GPT-4o | std | 205 | 103571 | 42932 |
| GPT-4o-mini | sec | 223 | 127230 | 59076 |
| GPT-4o-mini | std | 220 | 117161 | 48925 |
| GPT-5.6-sol | sec | 185 | 94607 | 183198 |
| GPT-5.6-sol | std | 186 | 89128 | 105426 |
| Claude Haiku 4.5 | sec | 190 | 116435 | 121569 |
| Claude Haiku 4.5 | std | 189 | 107807 | 94705 |
| Claude Sonnet 4.5 | sec | 189 | 115179 | 122577 |
| Claude Sonnet 4.5 | std | 189 | 107640 | 113139 |
| Claude Sonnet 5 | sec | 187 | 147021 | 231252 |
| Claude Sonnet 5 | std | 186 | 134768 | 84292 |

