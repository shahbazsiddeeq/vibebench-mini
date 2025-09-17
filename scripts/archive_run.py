#!/usr/bin/env python3
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
DEST = ROOT / "history" / STAMP
DEST.mkdir(parents=True, exist_ok=True)


def copy_if_exists(p: Path):
    if p.exists():
        shutil.copy2(p, DEST / p.name)


copy_if_exists(ROOT / "results.json")
copy_if_exists(ROOT / "results.csv")
copy_if_exists(ROOT / "scorecard.md")
if (ROOT / "reports").exists():
    shutil.copytree(ROOT / "reports", DEST / "reports")

# append to index.json
idx = ROOT / "history" / "index.json"
data = []
if idx.exists():
    data = json.loads(idx.read_text(encoding="utf-8"))
data.append({"stamp": STAMP, "path": f"history/{STAMP}"})
idx.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("Archived to", DEST)
