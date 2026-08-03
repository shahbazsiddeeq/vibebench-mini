"""src/solution.py

A small, self-contained parser for robots.txt content.

The public entry point is :func:`parse_robots`, which extracts the
allow/disallow rules and crawl-delay for a particular user-agent from a
robots.txt document.
"""

from __future__ import annotations

from typing import Dict, List, Optional


def _new_group() -> Dict:
    """Create an empty group structure."""
    return {
        "agents": set(),
        "allow": [],
        "disallow": [],
        "crawl_delay": None,
        "started_directives": False,
    }


def parse_robots(content: str, user_agent: str) -> Dict[str, object]:
    """Parse ``content`` (the text of a robots.txt file) and return the
    rules that apply to ``user_agent``.

    The return value is a dict of the form::

        {"allowed": [...], "disallowed": [...], "crawl_delay": float or None}
    """
    groups: List[Dict] = []
    current: Optional[Dict] = None

    for raw_line in content.splitlines():
        line = raw_line.strip()

        # Blank line ends the current group.
        if line == "":
            if current is not None:
                groups.append(current)
                current = None
            continue

        # Comments are ignored, but do NOT end the current group.
        if line.startswith("#"):
            continue

        if ":" not in line:
            # Malformed line, ignore it.
            continue

        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()

        if key == "user-agent":
            if value == "":
                continue
            agent_lower = value.lower()

            if current is None or current["started_directives"]:
                # Need to start a new group.
                if current is not None:
                    groups.append(current)
                current = _new_group()

            current["agents"].add(agent_lower)

        elif key in ("allow", "disallow"):
            if current is None:
                # Directive with no preceding user-agent: ignore.
                continue
            current["started_directives"] = True
            if value != "":
                current[key].append(value)

        elif key == "crawl-delay":
            if current is None:
                continue
            current["started_directives"] = True
            try:
                current["crawl_delay"] = float(value)
            except ValueError:
                pass
        else:
            # Unknown directive - ignore, but if we're already inside a
            # group it shouldn't break anything.
            continue

    if current is not None:
        groups.append(current)

    ua_lower = user_agent.lower()

    matched_group = None
    wildcard_group = None

    for group in groups:
        if ua_lower in group["agents"]:
            matched_group = group
            break
        if "*" in group["agents"] and wildcard_group is None:
            wildcard_group = group

    chosen = matched_group if matched_group is not None else wildcard_group

    if chosen is None:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}

    return {
        "allowed": list(chosen["allow"]),
        "disallowed": list(chosen["disallow"]),
        "crawl_delay": chosen["crawl_delay"],
    }
