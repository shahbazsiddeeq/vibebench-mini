#!/usr/bin/env python3
"""
Archive agent runs from .agent_runs/ into history/<tag>/<agent>/ with a manifest,
and optionally compress each agent snapshot to dist/archives/<tag>__<agent>.tar.gz.

Examples:
  python scripts/archive_run.py --agent openai-default --tag baseline-v1 --compress
  python scripts/archive_run.py --agent copyref --agent naive --tag local-20250924
  python scripts/archive_run.py --tag autoscan --compress   # archives all agents found
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_ROOT = ROOT / ".agent_runs"
HISTORY_ROOT = ROOT / "history"
ARCHIVE_ROOT = ROOT / "dist" / "archives"


def human_bytes(n: int) -> str:
    step = 1024.0
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < step:
            return f"{n:.1f} {unit}"
        n /= step
    return f"{n:.1f} PB"


def dir_size_bytes(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            try:
                total += p.stat().st_size
            except Exception:
                pass
    return total


def discover_agents() -> list[str]:
    if not AGENTS_ROOT.exists():
        return []
    return sorted([p.name for p in AGENTS_ROOT.iterdir() if p.is_dir()])


def copy_agent_run(agent: str, tag: str) -> dict:
    src = AGENTS_ROOT / agent
    if not src.exists():
        raise FileNotFoundError(f"Agent '{agent}' not found at {src}")

    dest = HISTORY_ROOT / tag / agent
    ignore = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.pyo")

    # Copy with merge semantics (dirs_exist_ok=True).
    shutil.copytree(src, dest, dirs_exist_ok=True, ignore=ignore)

    results_csv = src / "results.csv"
    meta = {
        "agent": agent,
        "src": str(src),
        "dest": str(dest),
        "results_csv_present": results_csv.exists(),
        "size_bytes": dir_size_bytes(dest),
        "tasks_count": len(list((dest / "tasks").rglob("task*"))),
    }
    return meta


def compress_agent(tag: str, agent: str) -> Path:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    # base_name is the archive path without extension; shutil adds .tar.gz for gztar
    base_name = ARCHIVE_ROOT / f"{tag}__{agent}"
    # root_dir/base_dir stores a clean top-level "<agent>/" inside the tar
    shutil.make_archive(
        base_name=str(base_name),
        format="gztar",
        root_dir=HISTORY_ROOT / tag,
        base_dir=agent,
    )
    return Path(f"{base_name}.tar.gz")


def write_manifest(tag: str, entries: list[dict]) -> None:
    outdir = HISTORY_ROOT / tag
    outdir.mkdir(parents=True, exist_ok=True)
    created = datetime.now().astimezone().isoformat(timespec="seconds")

    manifest = {
        "tag": tag,
        "created_at": created,
        "root": str(outdir),
        "agents": entries,
        "env": {"cwd": os.getcwd(), "python": sys.version.split()[0]},
    }
    (outdir / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    # A small human-friendly README
    lines = [
        f"# Archive: {tag}",
        "",
        f"- Created: `{created}`",
        f"- Agents: {', '.join(e['agent'] for e in entries)}",
        "",
        "| agent | tasks | size | results.csv |",
        "|---|---:|---:|---|",
    ]
    for e in entries:
        lines.append(
            f"| {e['agent']} | {e['tasks_count']} | {human_bytes(e['size_bytes'])} | "
            f"{'yes' if e['results_csv_present'] else 'no'} |"
        )
    (outdir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Archive .agent_runs into history/<tag>/<agent>/"
    )
    ap.add_argument(
        "--agent",
        action="append",
        default=None,
        help="Agent name under .agent_runs/ (repeatable). If omitted, archives all discovered agents.",
    )
    ap.add_argument(
        "--tag",
        default=None,
        help="Archive tag (folder name under history/). Default: agents-<YYYYmmdd-HHMMSS>.",
    )
    ap.add_argument(
        "--compress",
        action="store_true",
        help="Also create .tar.gz under dist/archives/ per agent.",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    agents = args.agent if args.agent else discover_agents()
    if not agents:
        print(
            "No agents found to archive. Did you run scripts/run_agents.py?",
            file=sys.stderr,
        )
        sys.exit(1)

    tag = args.tag or datetime.now().strftime("agents-%Y%m%d-%H%M%S")
    entries: list[dict] = []

    for a in agents:
        meta = copy_agent_run(a, tag)
        entries.append(meta)
        print(
            f"[ok] copied {a} -> history/{tag}/{a}  "
            f"tasks={meta['tasks_count']} size={human_bytes(meta['size_bytes'])}"
        )
        if args.compress:
            tarpath = compress_agent(tag, a)
            print(f"      compressed -> {tarpath}")

    write_manifest(tag, entries)
    print(f"\nDone. See: history/{tag}/README.md and MANIFEST.json")
    if args.compress:
        print(f"Archives in: {ARCHIVE_ROOT}")


if __name__ == "__main__":
    main()
