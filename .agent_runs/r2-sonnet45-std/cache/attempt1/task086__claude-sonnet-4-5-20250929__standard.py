def parse_robots(content, user_agent):
    """
    Parse a robots.txt document and return rules for the given user-agent.
    
    Returns a dict with keys: "allowed", "disallowed", "crawl_delay"
    """
    if not content or not content.strip():
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
    
    lines = content.split('\n')
    groups = []
    current_group = None
    
    for line in lines:
        # Strip whitespace
        line = line.strip()
        
        # Skip comments
        if line.startswith('#'):
            continue
        
        # Blank line ends current group
        if not line:
            if current_group is not None:
                groups.append(current_group)
                current_group = None
            continue
        
        # Parse the line
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip().lower()
            value = value.strip()
            
            if key == 'user-agent':
                # Start a new group or add to current group's user-agents
                if current_group is None:
                    current_group = {
                        'user_agents': [],
                        'allowed': [],
                        'disallowed': [],
                        'crawl_delay': None
                    }
                current_group['user_agents'].append(value)
            
            elif key == 'allow':
                # Only add non-empty values
                if value and current_group is not None:
                    current_group['allowed'].append(value)
            
            elif key == 'disallow':
                # Only add non-empty values
                if value and current_group is not None:
                    current_group['disallowed'].append(value)
            
            elif key == 'crawl-delay':
                if current_group is not None:
                    try:
                        current_group['crawl_delay'] = float(value)
                    except ValueError:
                        pass
    
    # Don't forget the last group if file doesn't end with blank line
    if current_group is not None:
        groups.append(current_group)
    
    # Find matching group (case-insensitive)
    user_agent_lower = user_agent.lower()
    matching_group = None
    wildcard_group = None
    
    for group in groups:
        for ua in group['user_agents']:
            if ua.lower() == user_agent_lower:
                matching_group = group
                break
            if ua == '*':
                wildcard_group = group
        if matching_group:
            break
    
    # Use specific match, fall back to wildcard, or return empty
    if matching_group:
        return {
            "allowed": matching_group['allowed'],
            "disallowed": matching_group['disallowed'],
            "crawl_delay": matching_group['crawl_delay']
        }
    elif wildcard_group:
        return {
            "allowed": wildcard_group['allowed'],
            "disallowed": wildcard_group['disallowed'],
            "crawl_delay": wildcard_group['crawl_delay']
        }
    else:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
