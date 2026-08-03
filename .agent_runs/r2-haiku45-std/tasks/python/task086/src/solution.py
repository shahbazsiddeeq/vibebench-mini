def parse_robots(content, user_agent):
    """
    Parse a robots.txt document and return rules for the given user-agent.
    
    Args:
        content: The robots.txt file content as a string
        user_agent: The user-agent to find rules for (case-insensitive)
    
    Returns:
        A dictionary with keys "allowed", "disallowed", and "crawl_delay"
    """
    lines = content.split('\n')
    
    # Parse groups
    groups = []
    current_group = None
    
    for line in lines:
        # Strip whitespace
        line = line.strip()
        
        # Skip empty lines - they end the current group
        if not line:
            if current_group is not None:
                groups.append(current_group)
                current_group = None
            continue
        
        # Skip comments
        if line.startswith('#'):
            continue
        
        # Parse directives
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            if key == 'user-agent':
                # Start a new group if we have a previous one
                if current_group is not None:
                    groups.append(current_group)
                current_group = {
                    'user_agents': [value.lower()],
                    'allowed': [],
                    'disallowed': [],
                    'crawl_delay': None
                }
            elif current_group is not None:
                if key == 'allow':
                    if value:  # Only add non-empty values
                        current_group['allowed'].append(value)
                elif key == 'disallow':
                    if value:  # Only add non-empty values
                        current_group['disallowed'].append(value)
                elif key == 'crawl-delay':
                    try:
                        current_group['crawl_delay'] = float(value)
                    except ValueError:
                        pass
                elif key == 'user-agent':
                    # Additional user-agent in same group
                    current_group['user_agents'].append(value.lower())
    
    # Don't forget the last group if file doesn't end with blank line
    if current_group is not None:
        groups.append(current_group)
    
    # Find matching group
    user_agent_lower = user_agent.lower()
    
    # First, try to find exact match
    for group in groups:
        if user_agent_lower in group['user_agents']:
            return {
                'allowed': group['allowed'],
                'disallowed': group['disallowed'],
                'crawl_delay': group['crawl_delay']
            }
    
    # Fall back to "*" group
    for group in groups:
        if '*' in group['user_agents']:
            return {
                'allowed': group['allowed'],
                'disallowed': group['disallowed'],
                'crawl_delay': group['crawl_delay']
            }
    
    # No matching group found
    return {
        'allowed': [],
        'disallowed': [],
        'crawl_delay': None
    }
