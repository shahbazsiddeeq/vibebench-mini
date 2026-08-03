# src/solution.py

def parse_robots(content, user_agent):
    user_agent = user_agent.lower()
    lines = content.splitlines()
    current_user_agents = []
    rules = {}
    default_rules = {"allowed": [], "disallowed": [], "crawl_delay": None}
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.lower().startswith('user-agent:'):
            current_user_agents = [ua.strip().lower() for ua in line[11:].split(',')]
            rules[tuple(current_user_agents)] = {"allowed": [], "disallowed": [], "crawl_delay": None}
            continue
        
        if not current_user_agents:
            continue
        
        if line.lower().startswith('allow:'):
            path = line[6:].strip()
            if path:
                for ua in current_user_agents:
                    rules[tuple(current_user_agents)]["allowed"].append(path)
            continue
        
        if line.lower().startswith('disallow:'):
            path = line[9:].strip()
            if path:
                for ua in current_user_agents:
                    rules[tuple(current_user_agents)]["disallowed"].append(path)
            continue
        
        if line.lower().startswith('crawl-delay:'):
            try:
                delay = float(line[12:].strip())
                for ua in current_user_agents:
                    rules[tuple(current_user_agents)]["crawl_delay"] = delay
            except ValueError:
                continue
    
    # Find the best matching rules
    for agents, rule in rules.items():
        if user_agent in agents:
            return rule
    
    # Fallback to wildcard rules
    for agents, rule in rules.items():
        if '*' in agents:
            return rule
    
    return default_rules
