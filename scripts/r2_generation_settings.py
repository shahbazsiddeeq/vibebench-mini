#!/usr/bin/env python3.12
"""Generation settings and API accounting for the r2 run.

This reports the settings that were actually used, not the settings
that were intended. Each `.agent_runs/r2-*/runinfo.json` records what the agent
configured at start up, and each `events.jsonl` records what every API call
returned. This script joins the two and reports, per configuration, the model
id, endpoint, temperature actually sent, output cap, token budget, token totals,
call counts, truncated calls and the distribution of finish reasons.

It reads only. It is cheap, it runs in seconds, and it is safe to run while the
generation is still writing, because a partially written last line of
`events.jsonl` is skipped and a configuration with fewer than 185 tasks is
labeled incomplete.

Output:
  reports/r2_generation_settings.md

Run:  python3.12 scripts/r2_generation_settings.py
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r2_repair_audit import (  # noqa: E402  (shared discovery and event parsing)
    EXPECTED_TASKS,
    REPORTS,
    discover_configs,
    read_json,
)

ROOT = Path(__file__).resolve().parents[1]


def scan_events(run_dir: Path) -> dict:
    """Aggregate every API call in one run directory."""
    agg = {
        "calls": 0,
        "errors": 0,
        "truncated": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "reasoning_tokens": 0,
        "cached_tokens": 0,
        "wall_s": 0.0,
        "finish_reasons": collections.Counter(),
        "error_types": collections.Counter(),
        "incomplete_reasons": collections.Counter(),
        "temperatures": collections.Counter(),
        "max_output_tokens": collections.Counter(),
        "calls_by_attempt": collections.Counter(),
        "tasks": set(),
        "tasks_attempt1": set(),
        "repair_decisions": 0,
        "repair_attempted": 0,
        "repair_results": 0,
        "cache_hits": 0,
        "no_program": 0,
        "budget_skips": 0,
        "bad_lines": 0,
    }
    path = run_dir / "events.jsonl"
    if not path.exists():
        return agg
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                agg["bad_lines"] += 1
                continue
            kind = ev.get("event")
            tid = ev.get("task_id")
            if tid:
                agg["tasks"].add(tid)
            if kind in ("api_call", "api_error"):
                failed = kind == "api_error" or bool(ev.get("error_type"))
                agg["calls"] += 1
                agg["calls_by_attempt"][ev.get("attempt")] += 1
                if ev.get("attempt") == 1 and tid and not failed:
                    agg["tasks_attempt1"].add(tid)
                if failed:
                    agg["errors"] += 1
                    agg["error_types"][ev.get("error_type") or "unknown"] += 1
                if ev.get("truncated") is True:
                    agg["truncated"] += 1
                if ev.get("incomplete_reason"):
                    agg["incomplete_reasons"][ev["incomplete_reason"]] += 1
                agg["finish_reasons"][str(ev.get("finish_reason"))] += 1
                for k in (
                    "prompt_tokens", "completion_tokens", "total_tokens",
                    "reasoning_tokens", "cached_tokens",
                ):
                    v = ev.get(k)
                    if isinstance(v, (int, float)):
                        agg[k] += int(v)
                w = ev.get("wall_s")
                if isinstance(w, (int, float)):
                    agg["wall_s"] += float(w)
                if "temperature" in ev:
                    agg["temperatures"][str(ev["temperature"])] += 1
                if ev.get("max_output_tokens") is not None:
                    agg["max_output_tokens"][str(ev["max_output_tokens"])] += 1
            elif kind == "repair_decision":
                agg["repair_decisions"] += 1
                if ev.get("repair_attempted") is True:
                    agg["repair_attempted"] += 1
            elif kind == "repair_result":
                agg["repair_results"] += 1
            elif kind == "cache_hit":
                agg["cache_hits"] += 1
            elif kind == "no_program":
                agg["no_program"] += 1
            elif kind == "budget_skip":
                agg["budget_skips"] += 1
    return agg


def dist(counter: collections.Counter) -> str:
    if not counter:
        return "none"
    return "; ".join(f"{k} {v}" for k, v in counter.most_common())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pattern", default="r2-*")
    ap.add_argument("--configs", default="", help="comma separated run names to keep")
    ap.add_argument("--out-dir", default=str(REPORTS))
    ap.add_argument("--expected-tasks", type=int, default=EXPECTED_TASKS)
    args = ap.parse_args()

    configs = discover_configs(args.pattern)
    if args.configs:
        keep = {c.strip() for c in args.configs.split(",") if c.strip()}
        configs = [
            c for c in configs
            if c["run"] in keep or c["run"].removeprefix("r2-") in keep
        ]
    if not configs:
        print("no configurations matched", file=sys.stderr)
        sys.exit(1)

    scans = {c["run"]: scan_events(c["dir"]) for c in configs}

    L: list[str] = []
    L.append("# Generation settings actually used (r2 run)")
    L.append("")
    L.append(
        "Produced by `scripts/r2_generation_settings.py`. The settings columns "
        "come from each run's `runinfo.json`, which the agent writes before the "
        "first call. The accounting columns come from each run's "
        "`events.jsonl`, which records one object per API call. The temperature "
        "column reports the value the client sent. A model that rejects the "
        "parameter is shown as provider default, and no temperature was sent for "
        "those runs."
    )
    L.append("")

    L.append("## Settings")
    L.append("")
    L.append(
        "| Configuration | Prompt | Model id | Provider | Endpoint | Temperature sent | "
        "Max output tokens | Token budget | Repair enabled | SDK | Status |"
    )
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for c in configs:
        info = c["runinfo"] or {}
        s = scans[c["run"]]
        n = len(s["tasks"])
        status = (
            "complete" if n >= args.expected_tasks
            else f"incomplete ({n}/{args.expected_tasks})"
        )
        # The temperature actually observed on the wire, when the calls recorded
        # one, otherwise the value declared at start up.
        temp_seen = dist(s["temperatures"]) if s["temperatures"] else str(
            info.get("temperature", "unknown")
        )
        if len(s["temperatures"]) == 1:
            temp_seen = next(iter(s["temperatures"]))
        L.append(
            f"| {c['label']} | {c['prompt']} | `{info.get('model', c['model_id'])}` | "
            f"{info.get('provider', '')} | `{info.get('endpoint', '')}` | {temp_seen} | "
            f"{info.get('max_output_tokens', '')} | {info.get('token_budget', '')} | "
            f"{info.get('repair_once', '')} | "
            f"{info.get('sdk', '')} {info.get('sdk_version', '')} | {status} |"
        )
    L.append("")

    L.append("## API accounting")
    L.append("")
    L.append(
        "| Configuration | Prompt | Tasks seen | API calls | First attempts | Repair calls | "
        "Errors | Truncated | Prompt tokens | Completion tokens | Total tokens | "
        "Reasoning tokens | Cached tokens |"
    )
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c in configs:
        s = scans[c["run"]]
        L.append(
            f"| {c['label']} | {c['prompt']} | {len(s['tasks'])} | {s['calls']} | "
            f"{s['calls_by_attempt'].get(1, 0)} | {s['calls_by_attempt'].get(2, 0)} | "
            f"{s['errors']} | {s['truncated']} | {s['prompt_tokens']} | "
            f"{s['completion_tokens']} | {s['total_tokens']} | "
            f"{s['reasoning_tokens']} | {s['cached_tokens']} |"
        )
    L.append("")
    L.append(
        "First attempts and repair calls are counts of API calls carrying "
        "attempt 1 and attempt 2. A retried call adds to the count, so these "
        "numbers can exceed the number of tasks."
    )
    L.append("")

    L.append("## Finish reasons and truncation")
    L.append("")
    L.append(
        "| Configuration | Prompt | Finish reason distribution | Truncated calls | "
        "Incomplete reasons | Error types |"
    )
    L.append("|---|---|---|---|---|---|")
    for c in configs:
        s = scans[c["run"]]
        L.append(
            f"| {c['label']} | {c['prompt']} | {dist(s['finish_reasons'])} | "
            f"{s['truncated']} | {dist(s['incomplete_reasons'])} | "
            f"{dist(s['error_types'])} |"
        )
    L.append("")
    L.append(
        "A truncated call is one the provider stopped at the output cap. The "
        "finish reason names differ by provider. The OpenAI Responses API "
        "reports `completed`, the Anthropic Messages API reports `end_turn`, and "
        "the OpenRouter chat completions API reports `stop`. All three mean the "
        "model finished on its own."
    )
    L.append("")

    L.append("## Cost ledgers")
    L.append("")
    L.append("| Configuration | Prompt | Requests | Input tokens | Output tokens |")
    L.append("|---|---|---|---|---|")
    for c in configs:
        led = read_json(c["dir"] / "cost_ledger.json") or {}
        L.append(
            f"| {c['label']} | {c['prompt']} | {led.get('requests', 'n/a')} | "
            f"{led.get('input_tokens', 'n/a')} | {led.get('output_tokens', 'n/a')} |"
        )
    L.append("")

    incomplete = [
        c["run"] for c in configs
        if len(scans[c["run"]]["tasks"]) < args.expected_tasks
    ]
    if incomplete:
        L.append("## Incomplete configurations")
        L.append("")
        L.append(
            "The following configurations had seen fewer than "
            f"{args.expected_tasks} tasks when this report was written, so their "
            "totals are a progress check and not a final result: "
            + ", ".join(incomplete)
            + "."
        )
        L.append("")
    bad = sum(scans[c["run"]]["bad_lines"] for c in configs)
    if bad:
        L.append(
            f"{bad} event lines could not be parsed and were skipped. A single "
            "such line at the end of a file is the tail of a record that was "
            "still being written."
        )
        L.append("")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "r2_generation_settings.md"
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
