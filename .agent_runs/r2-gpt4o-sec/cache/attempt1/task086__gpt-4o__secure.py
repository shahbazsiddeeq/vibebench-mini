# src/solution.py

def parse_robots(content, user_agent):
    import re

    # Normalize user_agent to lowercase for case-insensitive matching
    user_agent = user_agent.lower()

    # Initialize the default result
    default_result = {"allowed": [], "disallowed": [], "crawl_delay": None}

    # Split the content into lines and strip whitespace
    lines = content.splitlines()
    lines = [line.strip() for line in lines]

    # Initialize variables to track the current group
    current_agents = []
    current_rules = {"allowed": [], "disallowed": [], "crawl_delay": None}
    matched_group = None

    # Regular expressions for parsing lines
    user_agent_re = re.compile(r'^User-agent:\s*(.+)', re.I)
    allow_re = re.compile(r'^Allow:\s*(.*)', re.I)
    disallow_re = re.compile(r'^Disallow:\s*(.*)', re.I)
    crawl_delay_re = re.compile(r'^Crawl-delay:\s*(\d+(\.\d+)?)', re.I)

    for line in lines:
        if not line or line.startswith('#'):
            # Skip empty lines and comments
            continue

        user_agent_match = user_agent_re.match(line)
        allow_match = allow_re.match(line)
        disallow_match = disallow_re.match(line)
        crawl_delay_match = crawl_delay_re.match(line)

        if user_agent_match:
            # Start a new group if we encounter a User-agent line
            agent = user_agent_match.group(1).strip().lower()
            if matched_group is None and (agent == user_agent or agent == '*'):
                matched_group = current_rules
            current_agents.append(agent)
        elif allow_match:
            path = allow_match.group(1).strip()
            if path:
                current_rules["allowed"].append(path)
        elif disallow_match:
            path = disallow_match.group(1).strip()
            if path:
                current_rules["disallowed"].append(path)
        elif crawl_delay_match:
            delay = float(crawl_delay_match.group(1))
            current_rules["crawl_delay"] = delay

        # If we reach a blank line, reset the current group
        if not line:
            current_agents = []
            current_rules = {"allowed": [], "disallowed": [], "crawl_delay": None}

    # If no specific group matched, check for the wildcard group
    if matched_group is None:
        for agent in current_agents:
            if agent == '*':
                matched_group = current_rules
                break

    # Return the matched group or the default result
    return matched_group if matched_group is not None else default_result
