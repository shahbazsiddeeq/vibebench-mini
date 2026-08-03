"""
src/solution.py

A secure, self-contained robots.txt parser.

Only the Python standard library is used. Input is validated defensively
and no code execution (eval/exec) or external I/O is performed.
"""

from typing import Dict, List, Optional, Tuple


def _sanitize_line(raw_line: str) -> str:
    """Strip whitespace and control characters from a single line."""
    # Remove any surrounding whitespace; guard against extremely long lines
    # by truncating to a sane maximum length to avoid resource exhaustion.
    MAX_LINE_LENGTH = 8192
    line = raw_line[:MAX_LINE_LENGTH]
    return line.strip()


def parse_robots(content: str, user_agent: str) -> Dict[str, object]:
    """
    Parse a robots.txt document and return the rules applicable to the
    given user-agent.

    Args:
        content: The full text of a robots.txt file.
        user_agent: The user-agent string to match against groups.

    Returns:
        A dict with keys:
            - "allowed": list of allowed paths (strings)
            - "disallowed": list of disallowed paths (strings)
            - "crawl_delay": float or None

    Raises:
        TypeError: if arguments are not strings.
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(user_agent, str):
        raise TypeError("user_agent must be a string")

    # Cap total input size defensively to avoid pathological memory/time use.
    MAX_CONTENT_LENGTH = 5_000_000  # ~5MB, generous for a robots.txt file
    safe_content = content[:MAX_CONTENT_LENGTH]

    lines = safe_content.splitlines()

    groups: List[Tuple[List[str], Dict[str, object]]] = []

    current_agents: List[str] = []
    current_directives: Dict[str, object] = {
        "allow": [],
        "disallow": [],
        "crawl_delay": None,
    }
    collecting_agents = True  # True while still accepting User-agent lines

    def push_group() -> None:
        """Finalize the current group (if it has any agents) and reset state."""
        nonlocal current_agents, current_directives, collecting_agents
        if current_agents:
            groups.append((current_agents, current_directives))
        current_agents = []
        current_directives = {
            "allow": [],
            "disallow": [],
            "crawl_delay": None,
        }
        collecting_agents = True

    for raw_line in lines:
        line = _sanitize_line(raw_line)

        if not line:
            # Blank line ends the current group.
            push_group()
            continue

        if line.startswith("#"):
            # Full-line comment: ignore without ending the group.
            continue

        if ":" not in line:
            # Malformed directive line; ignore safely.
            continue

        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()

        # Strip a trailing inline comment from the value, if present.
        if "#" in value:
            value = value.split("#", 1)[0].strip()

        if key == "user-agent":
            if not collecting_agents:
                # A new group starts without a preceding blank line.
                push_group()
            current_agents.append(value.lower())
        elif key == "disallow":
            collecting_agents = False
            if value:
                current_directives["disallow"].append(value)
        elif key == "allow":
            collecting_agents = False
            if value:
                current_directives["allow"].append(value)
        elif key == "crawl-delay":
            collecting_agents = False
            try:
                current_directives["crawl_delay"] = float(value)
            except (ValueError, TypeError):
                # Invalid crawl-delay value; ignore safely.
                pass
        else:
            # Unknown/unsupported directive; ignore.
            pass

    # Push the final group after processing all lines.
    push_group()

    ua_lower = user_agent.lower()

    matched: Optional[Dict[str, object]] = None
    wildcard: Optional[Dict[str, object]] = None

    for agents, directives in groups:
        if ua_lower in agents:
            matched = directives
            break
        if wildcard is None and "*" in agents:
            wildcard = directives

    if matched is None:
        matched = wildcard

    if matched is None:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}

    return {
        "allowed": list(matched["allow"]),
        "disallowed": list(matched["disallow"]),
        "crawl_delay": matched["crawl_delay"],
    }
