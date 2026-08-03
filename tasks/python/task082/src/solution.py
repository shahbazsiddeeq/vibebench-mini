from __future__ import annotations

from pathlib import Path


def write_config(path: str, config: dict[str, dict[str, str]]) -> None:
    lines = []
    for section, pairs in config.items():
        lines.append(f"[{section}]")
        for k, v in pairs.items():
            sv = str(v)
            if "\n" in sv or "\r" in sv:
                raise ValueError(f"value for '{k}' must not contain line breaks")
            lines.append(f"{k}={sv}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
