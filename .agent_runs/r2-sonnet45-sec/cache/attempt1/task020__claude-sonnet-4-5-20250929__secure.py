def is_balanced(s: str) -> bool:
    """
    Check if all brackets ()[]{}  are properly nested and matched.
    
    Args:
        s: Input string to check
        
    Returns:
        True if all brackets are properly balanced, False otherwise
    """
    # Validate input
    if not isinstance(s, str):
        return False
    
    # Define matching pairs
    matching = {')': '(', ']': '[', '}': '{'}
    opening = set('([{')
    closing = set(')]}')
    
    # Stack to track opening brackets
    stack = []
    
    # Process each character
    for char in s:
        # Only process bracket characters
        if char in opening:
            stack.append(char)
        elif char in closing:
            # Check if we have a matching opening bracket
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()
        # Ignore non-bracket characters
    
    # All brackets should be matched (stack should be empty)
    return len(stack) == 0
