"""Utilities for parsing robots.txt content."""

from __future__ import annotations

import math
from typing import Optional, TypedDict


class RobotsRules(TypedDict):
    allowed: list[str]
    disallowed: list[str]
    crawl_delay: Optional[float]


class _Group(TypedDict):
    agents: list[str]
    allowed: list[str]
    disallowed: list[str]
    crawl_delay: Optional[float]


def parse_robots(content: str, user_agent: str) -> RobotsRules:
    """Parse robots.txt rules for the specified user-agent."""
    groups: list[_Group] = []

    agents: list[str] = []
    allowed: list[str] = []
    disallowed: list[str] = []
    crawl_delay: Optional[float] = None
    directives_started = False

    def finish_group() -> None:
        nonlocal agents, allowed, disallowed, crawl_delay, directives_started
        if agents:
            groups.append(
                {
                    "agents": agents,
                    "allowed": allowed,
                    "disallowed": disallowed,
                    "crawl_delay": crawl_delay,
                }
            )
        agents = []
        allowed = []
        disallowed = []
        crawl_delay = None
        directives_started = False

    for raw_line in content.splitlines():
        line = raw_line.strip().lstrip("\ufeff")

        if not line:
            finish_group()
            continue

        if line.startswith("#"):
            continue

        key, separator, value = line.partition(":")
        if not separator:
            continue

        key = key.strip().casefold()
        value = value.strip()

        if key == "user-agent":
            if agents and directives_started:
                finish_group()
            if value:
                agents.append(value.casefold())
            continue

        if not agents:
            continue

        if key == "allow":
            directives_started = True
            if value:
                allowed.append(value)
        elif key == "disallow":
            directives_started = True
            if value:
                disallowed.append(value)
        elif key == "crawl-delay":
            directives_started = True
            try:
                parsed_delay = float(value)
            except ValueError:
                continue
            if math.isfinite(parsed_delay):
                crawl_delay = parsed_delay

    finish_group()

    target = user_agent.strip().casefold()
    selected = [group for group in groups if target in group["agents"]]

    if not selected:
        selected = [group for group in groups if "*" in group["agents"]]

    result: RobotsRules = {
        "allowed": [],
        "disallowed": [],
        "crawl_delay": None,
    }

    for group in selected:
        result["allowed"].extend(group["allowed"])
        result["disallowed"].extend(group["disallowed"])
        if result["crawl_delay"] is None and group["crawl_delay"] is not None:
            result["crawl_delay"] = group["crawl_delay"]

    return result
