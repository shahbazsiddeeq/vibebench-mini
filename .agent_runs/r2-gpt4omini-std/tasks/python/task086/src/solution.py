def parse_robots(content, user_agent):
    user_agent = user_agent.lower()
    rules = {}
    current_agent = None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.startswith("User-agent:"):
            if current_agent is not None:
                rules[current_agent] = rules.get(current_agent, {})
            current_agent = line.split(":", 1)[1].strip().lower()
            rules[current_agent] = {"allowed": [], "disallowed": [], "crawl_delay": None}
        
        elif current_agent is not None:
            if line.startswith("Allow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    rules[current_agent]["allowed"].append(path)
            elif line.startswith("Disallow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    rules[current_agent]["disallowed"].append(path)
            elif line.startswith("Crawl-delay:"):
                try:
                    delay = float(line.split(":", 1)[1].strip())
                    rules[current_agent]["crawl_delay"] = delay
                except ValueError:
                    pass

    # Check for the specific user agent or fallback to '*'
    if user_agent in rules:
        return rules[user_agent]
    elif '*' in rules:
        return rules['*']
    else:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
