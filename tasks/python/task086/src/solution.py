from __future__ import annotations


def parse_robots(content: str, user_agent: str) -> dict:
    sections: dict[str, dict] = {}
    current_agents: list[str] = []
    for line in content.splitlines():
        line = line.strip()
        # A blank line ends the current group; a comment line does NOT.
        if not line:
            current_agents = []
            continue
        if line.startswith("#"):
            continue
        if line.lower().startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip().lower()
            current_agents.append(agent)
            for a in current_agents:
                if a not in sections:
                    sections[a] = {"allowed": [], "disallowed": [], "crawl_delay": None}
        elif line.lower().startswith("disallow:") and current_agents:
            path = line.split(":", 1)[1].strip()
            for a in current_agents:
                sections.setdefault(
                    a, {"allowed": [], "disallowed": [], "crawl_delay": None}
                )
                if path:
                    sections[a]["disallowed"].append(path)
        elif line.lower().startswith("allow:") and current_agents:
            path = line.split(":", 1)[1].strip()
            for a in current_agents:
                sections.setdefault(
                    a, {"allowed": [], "disallowed": [], "crawl_delay": None}
                )
                if path:
                    sections[a]["allowed"].append(path)
        elif line.lower().startswith("crawl-delay:") and current_agents:
            try:
                delay = float(line.split(":", 1)[1].strip())
                for a in current_agents:
                    sections.setdefault(
                        a, {"allowed": [], "disallowed": [], "crawl_delay": None}
                    )
                    sections[a]["crawl_delay"] = delay
            except ValueError:
                pass
    ua = user_agent.lower()
    if ua in sections:
        return sections[ua]
    return sections.get("*", {"allowed": [], "disallowed": [], "crawl_delay": None})
