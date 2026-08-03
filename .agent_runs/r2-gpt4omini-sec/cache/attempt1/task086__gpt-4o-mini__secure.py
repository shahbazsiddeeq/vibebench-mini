# src/solution.py

def parse_robots(content: str, user_agent: str) -> dict:
    if not isinstance(content, str) or not isinstance(user_agent, str):
        raise ValueError("Both content and user_agent must be strings.")
    
    user_agent = user_agent.lower()
    rules = {"allowed": [], "disallowed": [], "crawl_delay": None}
    current_group = None
    default_group = None

    for line in content.splitlines():
        line = line.strip()
        
        if not line or line.startswith('#'):
            continue  # Skip empty lines and comments

        if line.lower().startswith("user-agent:"):
            if current_group is not None:
                # Save the current group before starting a new one
                if current_group['user_agent'] == '*':
                    default_group = current_group
                else:
                    if current_group['user_agent'].lower() == user_agent:
                        rules = current_group['rules']
                    elif default_group is not None:
                        rules = default_group['rules']
            
            # Start a new group
            current_group = {
                'user_agent': line.split(':', 1)[1].strip(),
                'rules': {"allowed": [], "disallowed": [], "crawl_delay": None}
            }
        
        elif current_group is not None:
            if line.lower().startswith("allow:"):
                path = line.split(':', 1)[1].strip()
                if path:
                    current_group['rules']['allowed'].append(path)
            elif line.lower().startswith("disallow:"):
                path = line.split(':', 1)[1].strip()
                if path:
                    current_group['rules']['disallowed'].append(path)
            elif line.lower().startswith("crawl-delay:"):
                try:
                    delay = float(line.split(':', 1)[1].strip())
                    current_group['rules']['crawl_delay'] = delay
                except ValueError:
                    continue  # Ignore invalid crawl-delay values

    # Final check for the last group
    if current_group is not None:
        if current_group['user_agent'] == '*':
            default_group = current_group
        elif current_group['user_agent'].lower() == user_agent:
            rules = current_group['rules']
        elif default_group is not None:
            rules = default_group['rules']

    return rules
