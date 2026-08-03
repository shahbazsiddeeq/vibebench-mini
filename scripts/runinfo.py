#!/usr/bin/env python3
import json
import platform
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)


def sh(*cmd):
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return ""


tools = {
    "python": sh("python", "-V"),
    "pip": sh("python", "-m", "pip", "-V"),
    "pytest": sh("pytest", "--version"),
    "radon": sh("radon", "--version"),
    "flake8": sh("flake8", "--version"),
    "bandit": sh("bandit", "--version"),
    "pip-audit": sh("pip-audit", "--version"),
    "mutmut": sh("python", "-m", "mutmut", "--version"),
}

info = {
    "git_commit": sh("git", "rev-parse", "HEAD"),
    "git_status_porcelain": sh("git", "status", "--porcelain"),
    "version_file": (
        (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        if (ROOT / "VERSION").exists()
        else ""
    ),
    "platform": {
        "system": platform.system(),
        "release": platform.release(),
        "python": platform.python_version(),
        "processor": platform.processor(),
    },
    "tools": tools,
}

# Build the tools line separately to keep lint happy
tools_line = ", ".join([f"{k}={v}" for k, v in tools.items() if v])

(OUT / "runinfo.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
(OUT / "runinfo.md").write_text(
    "\n".join(
        [
            "### Run Info",
            f"- Git commit: `{info['git_commit']}`",
            f"- VBM version: `{info['version_file']}`",
            f"- Python: `{info['platform']['python']}` on {info['platform']['system']} {info['platform']['release']}",
            f"- Tools: {tools_line}",
            "",
            "<details><summary>git status --porcelain</summary>\n\n```\n"
            + info["git_status_porcelain"]
            + "\n```\n</details>",
        ]
    )
    + "\n",
    encoding="utf-8",
)
print("Wrote reports/runinfo.{json,md}")
