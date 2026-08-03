def parse_robots(content, user_agent):
    """
    Parse a robots.txt document and return rules for the given user-agent.
    
    Args:
        content: The robots.txt content as a string
        user_agent: The user-agent to get rules for
    
    Returns:
        A dictionary with keys "allowed", "disallowed", and "crawl_delay"
    """
    # Validate inputs
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(user_agent, str):
        raise TypeError("user_agent must be a string")
    
    # Sanitize user_agent to prevent injection attacks
    user_agent = user_agent.strip().lower()
    if not user_agent:
        raise ValueError("user_agent cannot be empty")
    
    # Parse the robots.txt content into groups
    groups = []
    current_group = None
    
    lines = content.split('\n')
    
    for line in lines:
        # Strip whitespace
        line = line.strip()
        
        # Skip comments (but don't end the current group)
        if line.startswith('#'):
            continue
        
        # Empty line ends the current group
        if not line:
            if current_group is not None:
                groups.append(current_group)
                current_group = None
            continue
        
        # Parse the line
        if ':' not in line:
            # Invalid line, skip it
            continue
        
        key, _, value = line.partition(':')
        key = key.strip().lower()
        value = value.strip()
        
        # User-agent line starts or continues a group
        if key == 'user-agent':
            if current_group is None:
                current_group = {
                    'user_agents': [],
                    'allowed': [],
                    'disallowed': [],
                    'crawl_delay': None
                }
            current_group['user_agents'].append(value.lower())
        
        # Directive lines (only valid within a group)
        elif current_group is not None:
            if key == 'allow':
                if value:  # Ignore empty values
                    current_group['allowed'].append(value)
            elif key == 'disallow':
                if value:  # Ignore empty values
                    current_group['disallowed'].append(value)
            elif key == 'crawl-delay':
                try:
                    # Parse crawl-delay as float
                    delay = float(value)
                    if delay >= 0:  # Only accept non-negative values
                        current_group['crawl_delay'] = delay
                except (ValueError, OverflowError):
                    # Invalid crawl-delay value, ignore it
                    pass
    
    # Don't forget the last group if file doesn't end with blank line
    if current_group is not None:
        groups.append(current_group)
    
    # Find the matching group
    matching_group = None
    wildcard_group = None
    
    for group in groups:
        if user_agent in group['user_agents']:
            matching_group = group
            break
        if '*' in group['user_agents']:
            wildcard_group = group
    
    # Use matching group, or fall back to wildcard, or return empty
    if matching_group is not None:
        result_group = matching_group
    elif wildcard_group is not None:
        result_group = wildcard_group
    else:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
    
    return {
        "allowed": result_group['allowed'][:],  # Return a copy
        "disallowed": result_group['disallowed'][:],  # Return a copy
        "crawl_delay": result_group['crawl_delay']
    }
