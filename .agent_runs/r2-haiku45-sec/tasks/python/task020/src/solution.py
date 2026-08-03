def is_balanced(s):
    """
    Check if all brackets ()[]{}  are properly nested and matched.
    
    Non-bracket characters are ignored.
    
    Args:
        s: A string to check for balanced brackets
        
    Returns:
        True if all brackets are properly nested and matched, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    # Stack to track opening brackets
    stack = []
    
    # Mapping of closing brackets to their corresponding opening brackets
    bracket_pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    opening_brackets = set(bracket_pairs.values())
    closing_brackets = set(bracket_pairs.keys())
    
    for char in s:
        if char in opening_brackets:
            # Push opening bracket onto stack
            stack.append(char)
        elif char in closing_brackets:
            # Check if stack is empty or top doesn't match
            if not stack or stack[-1] != bracket_pairs[char]:
                return False
            # Pop the matching opening bracket
            stack.pop()
        # Ignore all other characters
    
    # Stack should be empty if all brackets are balanced
    return len(stack) == 0
