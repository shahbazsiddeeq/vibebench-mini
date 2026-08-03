#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

CANDIDATES = [
    ROOT / ".agent_runs/openai-default/cost_ledger.jsonl",
    ROOT / ".agent_runs/openai-default/cost_ledger.json",
    ROOT / ".agent_runs/js/openai-default/cost_ledger.jsonl",
    ROOT / ".agent_runs/js/openai-default/cost_ledger.json",
]

PRICING_PATH = Path(os.environ.get("PRICING_JSON", ROOT / "configs/pricing.json"))


def _read_jsonl(path: Path) -> Iterable[dict]:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except Exception:
            continue


def _read_json(path: Path) -> Iterable[dict]:
    txt = path.read_text(encoding="utf-8").strip()
    try:
        obj = json.loads(txt)
    except Exception:
        return []
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        return [obj]
    return []


def _normalize(rec: dict, track_hint: Optional[str]) -> Optional[dict]:
    """Return a flat record with tokens & basic metadata."""
    # Try to identify track from path hint or embedded fields
    track = track_hint or rec.get("track") or rec.get("lang")

    # Typical shapes:
    # { ts, model, task, usage: {prompt_tokens, completion_tokens, total_tokens} }
    # or { ts, model, task, usage: {input_tokens, output_tokens, total_tokens} }
    usage = rec.get("usage") or {}
    inp = usage.get("prompt_tokens", usage.get("input_tokens"))
    out = usage.get("completion_tokens", usage.get("output_tokens"))
    tot = usage.get("total_tokens")

    # Some providers only provide total; best-effort split (leave out=None)
    if inp is None and out is None and isinstance(tot, (int, float)):
        inp = tot
        out = 0

    model = rec.get("model") or rec.get("model_name") or "unknown"
    task = rec.get("task") or rec.get("task_id") or ""

    if inp is None and out is None and tot is None:
        return None

    return {
        "ts": rec.get("ts") or rec.get("timestamp"),
        "track": track,
        "model": model,
        "task": task,
        "input_tokens": float(inp) if inp is not None else math.nan,
        "output_tokens": float(out) if out is not None else math.nan,
        "total_tokens": float(tot) if tot is not None else math.nan,
    }


def _collect() -> pd.DataFrame:
    rows = []
    for p in CANDIDATES:
        if not p.exists():
            continue
        track_hint = (
            "python" if "/openai-default/" in str(p) and "/js/" not in str(p) else None
        )
        track_hint = "js" if "/js/openai-default/" in str(p) else track_hint
        loader = _read_jsonl if p.suffix == ".jsonl" else _read_json
        for rec in loader(p):
            flat = _normalize(rec, track_hint)
            if flat:
                rows.append(flat)
    if not rows:
        return pd.DataFrame(
            columns=[
                "ts",
                "track",
                "model",
                "task",
                "input_tokens",
                "output_tokens",
                "total_tokens",
            ]
        )
    df = pd.DataFrame(rows)
    # Backfill total if missing
    if "total_tokens" in df.columns:
        mask = (
            df["total_tokens"].isna()
            & df["input_tokens"].notna()
            & df["output_tokens"].notna()
        )
        df.loc[mask, "total_tokens"] = (
            df.loc[mask, "input_tokens"] + df.loc[mask, "output_tokens"]
        )
    return df


def _load_pricing() -> dict:
    if not PRICING_PATH.exists():
        return {}
    try:
        data = json.loads(PRICING_PATH.read_text(encoding="utf-8"))
        # Expect {"model": {"in": rate_per_token, "out": rate_per_token}}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _estimate_cost(df: pd.DataFrame, pricing: dict) -> pd.DataFrame:
    df = df.copy()
    df["cost_usd"] = pd.NA
    for model, rates in pricing.items():
        rin = float(rates.get("in", 0.0))
        rout = float(rates.get("out", 0.0))
        mask = df["model"] == model
        if not mask.any():
            continue
        inp = df.loc[mask, "input_tokens"].astype(float)
        out = df.loc[mask, "output_tokens"].astype(float)
        # If only total is present, attribute all to input side (conservative).
        inp = inp.fillna(df.loc[mask, "total_tokens"].astype(float))
        out = out.fillna(0.0)
        df.loc[mask, "cost_usd"] = inp * rin + out * rout
    return df


def main() -> None:
    df = _collect()
    if df.empty:
        print("No cost logs found. Run agents to produce cost_ledger.* first.")
        return

    pricing = _load_pricing()
    dfc = _estimate_cost(df, pricing) if pricing else df.assign(cost_usd=pd.NA)

    # Per-model summary (overall and by track)
    # def _agg(g: pd.DataFrame) -> pd.Series:
    #     return pd.Series(
    #         {
    #             "calls": len(g),
    #             "input_tokens": g["input_tokens"].sum(skipna=True),
    #             "output_tokens": g["output_tokens"].sum(skipna=True),
    #             "total_tokens": g["total_tokens"].sum(skipna=True),
    #             "cost_usd": g["cost_usd"].sum(skipna=True) if "cost_usd" in g else pd.NA,
    #         }
    #     )

    # overall = dfc.groupby("model", dropna=False).apply(_agg).reset_index()
    # by_track = (
    #     dfc.groupby(["track", "model"], dropna=False).apply(_agg).reset_index().sort_values(["track", "model"])
    # )
    # ensure numeric for sums
    for col in ("input_tokens", "output_tokens", "total_tokens", "cost_usd"):
        if col in dfc.columns:
            dfc[col] = pd.to_numeric(dfc[col], errors="coerce")

    # Overall by model (no FutureWarning)
    overall = dfc.groupby("model", dropna=False, as_index=False).agg(
        calls=("model", "size"),
        input_tokens=("input_tokens", "sum"),
        output_tokens=("output_tokens", "sum"),
        total_tokens=("total_tokens", "sum"),
        cost_usd=("cost_usd", "sum"),
    )

    # By track & model (no FutureWarning)
    by_track = (
        dfc.groupby(["track", "model"], dropna=False, as_index=False)
        .agg(
            calls=("model", "size"),
            input_tokens=("input_tokens", "sum"),
            output_tokens=("output_tokens", "sum"),
            total_tokens=("total_tokens", "sum"),
            cost_usd=("cost_usd", "sum"),
        )
        .sort_values(["track", "model"])
    )

    # Write CSVs
    overall.to_csv(OUT / "agents_costs.csv", index=False)
    by_track.to_csv(OUT / "agents_costs_by_track.csv", index=False)

    # Markdown (compact)
    def _fmt(v) -> str:
        if pd.isna(v):
            return ""
        try:
            return f"{float(v):.4f}"
        except Exception:
            return str(v)

    lines = [
        "## Agents — Cost & Token Summary\n",
        "### Overall by model",
        "| Model | Calls | Input toks | Output toks | Total toks | Est. cost (USD) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _, r in overall.iterrows():
        lines.append(
            f"| {r['model']} | {int(r['calls'])} | {int(r['input_tokens'])} | "
            f"{int(r['output_tokens'])} | {int(r['total_tokens'])} | {_fmt(r['cost_usd'])} |"
        )

    lines += [
        "",
        "### By track & model",
        "| Track | Model | Calls | Input toks | Output toks | Total toks | Est. cost (USD) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for _, r in by_track.iterrows():
        lines.append(
            f"| {r['track'] or ''} | {r['model']} | {int(r['calls'])} | {int(r['input_tokens'])} | "
            f"{int(r['output_tokens'])} | {int(r['total_tokens'])} | {_fmt(r['cost_usd'])} |"
        )

    (OUT / "agents_costs.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        "Wrote:",
        OUT / "agents_costs.md",
        OUT / "agents_costs.csv",
        OUT / "agents_costs_by_track.csv",
    )


if __name__ == "__main__":
    main()
