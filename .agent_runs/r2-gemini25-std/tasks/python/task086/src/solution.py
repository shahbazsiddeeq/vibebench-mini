def parse_robots(content, user_agent):
    """
    Parses a robots.txt document and returns the rules for the given user-agent.

    Args:
        content (str): The content of the robots.txt file.
        user_agent (str): The user-agent string to match.

    Returns:
        dict: A dictionary with "allowed", "disallowed" (lists of paths),
              and "crawl_delay" (float or None).
    """
    groups = []
    current_group = None

    for line in content.splitlines():
        line = line.strip()

        # Ignore comments
        if '#' in line:
            line = line.split('#', 1)[0].strip()

        if not line:
            # Blank line ends the current group
            if current_group:
                groups.append(current_group)
                current_group = None
            continue

        parts = line.split(':', 1)
        if len(parts) < 2:
            continue

        directive = parts[0].strip().lower()
        value = parts[1].strip()

        if directive == "user-agent":
            if current_group:
                groups.append(current_group)
            current_group = {
                "user_agents": [value.lower()],
                "allowed": [],
                "disallowed": [],
                "crawl_delay": None
            }
        elif current_group:
            if directive == "allow":
                if value:
                    current_group["allowed"].append(value)
            elif directive == "disallow":
                if value:
                    current_group["disallowed"].append(value)
            elif directive == "crawl-delay":
                try:
                    current_group["crawl_delay"] = float(value)
                except ValueError:
                    pass  # Ignore invalid crawl-delay values

    if current_group:
        groups.append(current_group)

    # Find the best matching group
    matching_group = None
    wildcard_group = None

    for group in groups:
        if user_agent.lower() in group["user_agents"]:
            matching_group = group
            break
        if "*" in group["user_agents"]:
            wildcard_group = group

    selected_group = matching_group if matching_group else wildcard_group

    if selected_group:
        return {
            "allowed": selected_group["allowed"],
            "disallowed": selected_group["disallowed"],
            "crawl_delay": selected_group["crawl_delay"]
        }
    else:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
