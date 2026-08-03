"""
Robots.txt Parser Module

Parses robots.txt documents and extracts rules for specific user-agents.
"""

from typing import Dict, List, Optional, Union


def parse_robots(content: str, user_agent: str) -> Dict[str, Union[List[str], Optional[float]]]:
    """
    Parse a robots.txt document and return rules for the given user-agent.
    
    Args:
        content: The robots.txt file content as a string
        user_agent: The user-agent to match (case-insensitive)
    
    Returns:
        A dictionary with keys:
        - "allowed": list of allowed paths
        - "disallowed": list of disallowed paths
        - "crawl_delay": float or None
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(user_agent, str):
        raise TypeError("user_agent must be a string")
    
    # Normalize user_agent for matching
    user_agent_lower = user_agent.lower()
    
    # Parse the content into groups
    groups = _parse_groups(content)
    
    # Find matching group
    matching_group = None
    
    # First, try to find an exact match (case-insensitive)
    for group in groups:
        if any(agent.lower() == user_agent_lower for agent in group["user_agents"]):
            matching_group = group
            break
    
    # If no exact match, fall back to "*"
    if matching_group is None:
        for group in groups:
            if any(agent.lower() == "*" for agent in group["user_agents"]):
                matching_group = group
                break
    
    # Build result
    if matching_group is None:
        return {"allowed": [], "disallowed": [], "crawl_delay": None}
    
    return {
        "allowed": matching_group["allowed"],
        "disallowed": matching_group["disallowed"],
        "crawl_delay": matching_group["crawl_delay"],
    }


def _parse_groups(content: str) -> List[Dict]:
    """
    Parse robots.txt content into groups.
    
    Args:
        content: The robots.txt file content
    
    Returns:
        A list of group dictionaries
    """
    groups = []
    lines = content.split("\n")
    
    current_group = None
    
    for line in lines:
        # Strip whitespace
        stripped = line.strip()
        
        # Skip empty lines - they end the current group
        if not stripped:
            if current_group is not None and current_group["user_agents"]:
                groups.append(current_group)
                current_group = None
            continue
        
        # Skip comments
        if stripped.startswith("#"):
            continue
        
        # Parse directives
        if ":" not in stripped:
            continue
        
        key, _, value = stripped.partition(":")
        key = key.strip().lower()
        value = value.strip()
        
        # Handle User-agent directive
        if key == "user-agent":
            # If we have a previous group with user-agents, save it
            if current_group is not None and current_group["user_agents"]:
                groups.append(current_group)
            # Start a new group
            current_group = {
                "user_agents": [value],
                "allowed": [],
                "disallowed": [],
                "crawl_delay": None,
            }
        
        # Handle other directives only if we're in a group
        elif current_group is not None:
            if key == "allow":
                if value:  # Only add non-empty values
                    current_group["allowed"].append(value)
            elif key == "disallow":
                if value:  # Only add non-empty values
                    current_group["disallowed"].append(value)
            elif key == "crawl-delay":
                try:
                    current_group["crawl_delay"] = float(value)
                except (ValueError, TypeError):
                    # Invalid crawl-delay value, ignore it
                    pass
            elif key == "user-agent":
                # Additional user-agent in same group
                current_group["user_agents"].append(value)
    
    # Don't forget the last group if it exists
    if current_group is not None and current_group["user_agents"]:
        groups.append(current_group)
    
    return groups
