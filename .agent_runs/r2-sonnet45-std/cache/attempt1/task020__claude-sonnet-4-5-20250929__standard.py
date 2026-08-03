def is_balanced(s):
    """
    Check if all brackets ()[]{}  are properly nested and matched.
    
    Args:
        s: A string containing brackets and other characters
        
    Returns:
        True if brackets are balanced, False otherwise
    """
    stack = []
    
    # Map closing brackets to their corresponding opening brackets
    matching = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    opening = set('([{')
    closing = set(')]}')
    
    for char in s:
        if char in opening:
            stack.append(char)
        elif char in closing:
            # If stack is empty or top doesn't match, it's unbalanced
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()
        # Ignore all other characters
    
    # Stack should be empty if all brackets are matched
    return len(stack) == 0
