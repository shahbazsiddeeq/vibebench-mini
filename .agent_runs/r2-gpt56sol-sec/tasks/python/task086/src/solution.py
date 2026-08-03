"""Robots.txt parsing utilities."""

from __future__ import annotations

import math
from typing import Optional, TypedDict


class RobotsRules(TypedDict):
    allowed: list[str]
    disallowed: list[str]
    crawl_delay: Optional[float]


def parse_robots(content: str, user_agent: str) -> RobotsRules:
    """Parse robots.txt content and return rules matching *user_agent*.

    Matching is case-insensitive and exact. Specific matching groups take
    precedence over wildcard groups. Rules from multiple matching groups are
    combined in document order.
    """
    empty: RobotsRules = {
        "allowed": [],
        "disallowed": [],
        "crawl_delay": None,
    }

    if not isinstance(content, str) or not isinstance(user_agent, str):
        return empty.copy()

    requested_agent = user_agent.strip().casefold()
    if not requested_agent or "\x00" in requested_agent:
        return empty.copy()

    groups: list[tuple[list[str], list[str], list[str], Optional[float]]] = []

    agents: list[str] = []
    allowed: list[str] = []
    disallowed: list[str] = []
    crawl_delay: Optional[float] = None
    directives_started = False

    def finish_group() -> None:
        nonlocal agents, allowed, disallowed, crawl_delay, directives_started
        if agents:
            groups.append((agents, allowed, disallowed, crawl_delay))
        agents = []
        allowed = []
        disallowed = []
        crawl_delay = None
        directives_started = False

    for raw_line in content.splitlines():
        line = raw_line.strip()

        if not line:
            finish_group()
            continue

        if line.startswith("#"):
            continue

        if ":" not in line:
            continue

        raw_name, raw_value = line.split(":", 1)
        name = raw_name.strip().casefold()
        value = raw_value.strip()

        if name == "user-agent":
            if directives_started:
                finish_group()

            normalized_agent = value.casefold()
            if normalized_agent and "\x00" not in normalized_agent:
                agents.append(normalized_agent)
            continue

        if name not in {"allow", "disallow", "crawl-delay"}:
            continue

        if not agents:
            continue

        directives_started = True

        if name == "allow":
            if value and "\x00" not in value:
                allowed.append(value)
        elif name == "disallow":
            if value and "\x00" not in value:
                disallowed.append(value)
        elif value:
            try:
                parsed_delay = float(value)
            except (TypeError, ValueError, OverflowError):
                continue
            if math.isfinite(parsed_delay) and parsed_delay >= 0:
                crawl_delay = parsed_delay

    finish_group()

    specific_groups = [
        group for group in groups if requested_agent in group[0]
    ]
    selected_groups = specific_groups or [
        group for group in groups if "*" in group[0]
    ]

    result: RobotsRules = {
        "allowed": [],
        "disallowed": [],
        "crawl_delay": None,
    }

    for _, group_allowed, group_disallowed, group_delay in selected_groups:
        result["allowed"].extend(group_allowed)
        result["disallowed"].extend(group_disallowed)
        if result["crawl_delay"] is None and group_delay is not None:
            result["crawl_delay"] = group_delay

    return result
