import collections

def parse_robots(content, user_agent):
    """
    Parses a robots.txt document and returns the rules for the given user-agent.

    Args:
        content (str): The content of the robots.txt file.
        user_agent (str): The user-agent string to match rules against.

    Returns:
        dict: A dictionary with keys "allowed", "disallowed", and "crawl_delay".
              Example: {"allowed": list, "disallowed": list, "crawl_delay": float|None}.
    """
    if not isinstance(content, str) or not isinstance(user_agent, str):
        raise TypeError("content and user_agent must be strings")

    # Normalize user_agent for case-insensitive matching
    normalized_user_agent = user_agent.lower()

    groups = collections.defaultdict(lambda: {"allowed": [], "disallowed": [], "crawl_delay": None})
    current_agents = []
    
    lines = content.splitlines()

    for line in lines:
        # Remove comments
        comment_start = line.find('#')
        if comment_start != -1:
            line = line[:comment_start]
        
        line = line.strip()

        if not line:  # Blank line ends the current group
            current_agents = []
            continue

        parts = line.split(':', 1)
        if len(parts) != 2:
            continue # Malformed line, ignore

        directive = parts[0].strip().lower()
        value = parts[1].strip()

        if directive == "user-agent":
            # If we encounter a new User-agent, it starts a new group
            # or adds to the current group if it's the first directive
            # in a sequence of User-agent lines.
            if not current_agents: # Start of a new group
                current_agents = [value.lower()]
            else: # Add to the current group
                current_agents.append(value.lower())
        elif current_agents: # Apply directives to the current group(s)
            for agent in current_agents:
                if directive == "allow":
                    if value:
                        groups[agent]["allowed"].append(value)
                elif directive == "disallow":
                    if value:
                        groups[agent]["disallowed"].append(value)
                elif directive == "crawl-delay":
                    try:
                        delay = float(value)
                        if delay >= 0: # Crawl-delay must be non-negative
                            groups[agent]["crawl_delay"] = delay
                    except ValueError:
                        pass # Ignore invalid crawl-delay values

    # Find the best matching group
    if normalized_user_agent in groups:
        return groups[normalized_user_agent]
    elif "*" in groups:
        return groups["*"]
    else:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
